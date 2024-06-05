
import os
from supabase import create_client, Client
from dotenv import load_dotenv

import time


def get_all_email_addresses(actor_input=None):
    """ log in as admin, get all email addresses """
    emails = []
    # load_dotenv()

    # url: str = os.environ.get("SUPABASE_URL")
    # key: str = os.environ.get("DANGER_SUPABASE_SERVICE")  # service role
    url = actor_input["supa_url"]
    key = actor_input["supa_service"]
    supabase: Client = create_client(url, key)
    response = supabase.table('all_users').select("email_address").execute()
    emails = [list(d.values())[0] for d in response.data]  # list of dicts
    return emails
