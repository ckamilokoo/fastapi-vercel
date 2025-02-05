import os
from supabase import create_client, Client

url: str = "https://kasavcuflkptbqewqrmv.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imthc2F2Y3VmbGtwdGJxZXdxcm12Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIwMDI1NTMsImV4cCI6MjA0NzU3ODU1M30.KL5OefuVJ8az1gfTkGV3gVda__OIUhPDjxAw7tlUQsA"
supabase: Client = create_client(url, key)


