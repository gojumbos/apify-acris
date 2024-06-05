

""" EMAIL """
import os
import pickle
from typing import List

import boto3
from dotenv import load_dotenv

from supa import get_all_email_addresses
from datetime import datetime

from airium import Airium


class EmailInterface:

    def __init__(self, from_address=None,
                 email_addresses=None,
                 scrape_date="",
                 actor_input=None):
        load_dotenv()
        # DRB 6/5 - had to get keys from actor input, then add to os.env
        os.environ["AWS_ACCESS_KEY_ID"] = actor_input["aws_key"]
        os.environ["AWS_SECRET_ACCESS_KEY"] = actor_input["aws_secret"]
        # Set your AWS region
        aws_region = 'us-east-1'
        # self.from_addr = os.getenv('FROM_ADDRESS')  # returns str
        self.from_addr = actor_input['from_addr']

        self.scrape_date = scrape_date

        # Create an SES client
        self.ses_client = boto3.client('ses', region_name=aws_region)

        """ SUPABASE """
        self.email_addresses = email_addresses
        if email_addresses is None:
            self.email_addresses = get_all_email_addresses(actor_input=actor_input)


        return

    def send_all_emails(self, all_data: List, email_subject='NYC Transactions - Test',
                        email_addresses=None,
                        style=None):
        """
        given list of all mortgage and deed data,
        format string and send email
        to all gathered addresses
        """

        if style is None:
            email_body = self.basic_format_email_body(all_data=all_data)
        else:
            email_body = self.format_email_body(all_data=all_data)

        for addr in self.email_addresses:
            try:
                self.send_email(email_body=email_body,
                                ses_client=self.ses_client,
                                email_subject=email_subject,
                                recipient_email=addr,
                                sender_email=self.from_addr)
            except BaseException as e:
                print(e, "bad email")

    def basic_format_email_body(self, all_data: List, date=""):
        """
        """
        s = str(self.scrape_date) + " \n"
        s += "\n ADDR / BORO / AMT / Party 1 / Party 2 / Doc ID No. \n"
        ctr = 0
        for li in all_data:
            if ctr % 5 == 0:
                print('\n')
            sub = ""
            for x in li:
                x = str(x)
                if x[0] == "$":
                    x = " " + x
                sub += " / " + x
            sub += "\n"
            s += sub

        return s

    def format_email_body(self, all_data: List):
        a = Airium()
        with a.table(id='all_data'):
            with a.tr(klass='header_row'):
                a.th(_t='no.')
                a.th(_t='Address')
                a.th(_t='Boro')
                a.th(_t='Amount')
                a.th(_t='Party 1')
                a.th(_t='Party 2')
                a.th(_t='Doc ID No.')

            for li in all_data:
                li = str(li)
                with a.tr():
                    a.td(_t=li)

            # with a.tr():
            #     a.td(_t='1.')
            #     a.td(id='jbl', _t='Jill')
            #     a.td(_t='Smith')  # can use _t or text
        return str(a)


    def send_email(self,
                   email_body: str,
                   ses_client,
                   email_subject='NYC Transactions - Test',
                   recipient_email='nyctransactions@gmail.com',
                   sender_email=None,):
        # Specify the email subject and body
        # email_subject = 'Test Email'
        # email_body = 'This is a test email sent from AWS SES using Python.'

        # Send the email
        response = ses_client.send_email(
            Source=self.from_addr,
            Destination={
                'ToAddresses': [recipient_email],
            },
            Message={
                'Subject': {'Data': email_subject},
                'Body': {'Text': {'Data': email_body}},
            }
        )

        print("Email sent! Message ID:", response['MessageId'])

    def test_send_email(self, email_body="TEST BODY",
                        email_subject='NYC Transactions - Test',
                        recipient_email='drborcich@gmail.com',
                        sender_email=None,):

        email_body = self.basic_format_email_body(all_data=[""], date="01/02/2024")

        self.send_email(email_body=email_body,
                        ses_client=self.ses_client,
                        email_subject=email_subject,
                        recipient_email=recipient_email)
