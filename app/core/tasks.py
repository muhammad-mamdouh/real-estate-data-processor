# -*- coding: utf-8 -*-
import csv

from celery import Task
from decimal import Decimal
import logging

from decouple import config
import pandas as pd

from app.settings.celery import app

from django.core.mail import send_mail
from django.utils import timezone

from .models import AbstractUnitType, Document, Portfolio, Asset, Unit
from .utils import logging_message

QUEUE_TASKS_LOGGER = logging.getLogger("queue_tasks")


class PortfolioDataProcessorTask(Task):
    """
    Processes the portfolio data uploaded into the sheets to be saved to the DB
    """

    def determine_csv_delimiter(self, doc_obj):
        """
        :param doc_obj: csv document to be processed
        :return: the delimiter used at the csv sheet or False if there is any problem
        """
        try:
            as_string = doc_obj.file.read().decode("utf-8")
            dialect = csv.Sniffer().sniff(as_string)
            doc_obj.file.seek(0)
            return dialect.delimiter
        except:
            return False

    def _unit_type(self, unit_type):
        """
        :param unit_type: unit type entered at the document
        :return unit type from the choices of the abstract unit type model
        """
        if unit_type == "RESIDENTIAL":
            return AbstractUnitType.RESIDENTIAL
        elif unit_type == "OFFICE":
            return AbstractUnitType.OFFICE
        elif unit_type == "RETAIL":
            return AbstractUnitType.RETAIL
        else:
            return AbstractUnitType.COMMERCIAL

    def accumulate_df(self, doc_obj):
        """
        :param doc_obj: document to be processed
        :return: data frame using pandas package
        """
        doc_type = "csv" if doc_obj.file.name.endswith(".csv") else "excel"

        if doc_type == "excel":
            df = pd.read_excel(doc_obj.file)
        else:
            df = pd.read_csv(doc_obj.file, delimiter=self.determine_csv_delimiter(doc_obj))

        return df

    def reformat_lease_start_date(self, lease_date):
        """
        Reformat provided lease start date field to be stored to a valid date object at the db
        :param lease_date: dotted string date
        :return valid date format to be save to a DateField
        """
        lease_date_str = str(lease_date)
        d, m, y = lease_date_str.split(".")
        lease_date_year = f"20{y}" if int(timezone.now().year) - int(f"20{y}") >= 0 else f"19{y}"
        return f"{lease_date_year}-{m}-{d}"

    def reformat_lease_end_date(self, lease_date):
        """
        Reformat provided lease end date field to be stored to a valid date object at the db
        :param lease_date: dotted string date
        :return valid date format to be save to a DateField
        """
        lease_date_str = str(lease_date)
        d, m, y = lease_date_str.split(".")
        return f"20{y}-{m}-{d}"

    def follow_up_email(self, is_passed):
        """
        Sends a follow up email upon finishing the processing of the task
        :param is_passed: is the file passed processing successfully or not
        """
        status = "Your file processed successfully." if is_passed else "Your file failed processing, please try again."
        message = "Dear User\n\n" + f"{status}\n\n" + "Kind regards,"

        return send_mail(
                from_email=config("MAIL_SENDER"),
                recipient_list=[config("MAIL_RECEIVER")],
                subject="[Real Estate File Processing Status]",
                message=message
        )

    def run(self, doc_id, *args, **kwargs):
        """
        :param doc_id: the uploaded document object that's passed for processing
        :return Send email after processing
        """

        mail_receiver = config("MAIL_RECEIVER")
        passed = True

        try:
            doc_obj = Document.objects.get(id=int(doc_id))
            df = self.accumulate_df(doc_obj)
            rows_count = max(df.count())

            for index in range(rows_count):
                portfolio, __ = Portfolio.objects.update_or_create(name=df.portfolio[index])
                asset, asset_created = Asset.objects.get_or_create(
                        portfolio=portfolio, reference=df.asset_ref[index], city=df.asset_city[index],
                        address=df.asset_address[index], zipcode=df.asset_zipcode[index],
                        is_restricted=df.asset_is_restricted[index], year_of_construction=df.asset_yoc[index]
                )

                unit_dict = {
                    "asset": asset,
                    "reference": df.unit_ref[index],
                    "is_rented": str(df.unit_is_rented[index]).capitalize(),
                    "size": int(df.unit_size[index]),
                    "unit_type": self._unit_type(df.unit_type[index])
                }
                if not pd.isnull(df.unit_tenant[index]):
                    unit_dict.update({"tenant": df.unit_tenant[index]})
                    unit_dict.update({"rent": Decimal(df.unit_rent[index])})
                    unit_dict.update({"lease_start": self.reformat_lease_start_date(df.unit_lease_start[index])})
                if not pd.isnull(df.unit_lease_end[index]):
                    unit_dict.update({"lease_end": self.reformat_lease_end_date(df.unit_lease_end[index])})

                unit = Unit.objects.filter(
                        reference=df.unit_ref[index], unit_type=self._unit_type(df.unit_type[index])
                )

                if unit.exists():
                    if not unit.filter(**unit_dict).exists():
                        current_time = timezone.now()
                        unit_dict.update({"updated_at": current_time})
                        unit.update(**unit_dict)
                        asset.updated_at = current_time
                        asset.save()
                else:
                    Unit.objects.create(**unit_dict)

            QUEUE_TASKS_LOGGER.debug(
                    f"[PortfolioDataProcessorTask - PASSED]\nProcessed successfully and mail sent to {mail_receiver}"
            )
        except (Document.DoesNotExist, Exception) as err:
            QUEUE_TASKS_LOGGER.debug(
                    f"[PortfolioDataProcessorTask - FAILED]\n"
                    f"Processing failure and mail sent to {mail_receiver}\nError{err.args[0]}"
            )
            passed = False

        self.follow_up_email(passed)
        return None


PortfolioDataProcessorTask = app.register_task(PortfolioDataProcessorTask())
