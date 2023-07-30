from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

import streamlit as st
import supabase
import pandas as pd
import json


class SupabaseConnection(ExperimentalBaseConnection[supabase.create_client]):
    def _connect(_self, **kwargs) -> supabase.create_client:

        SupabaseConnection.db = st.secrets["supabase_database"]
        # Establishes connection
        url = st.secrets["supabase_url"]
        key = st.secrets["supabase_key"]
        return supabase.create_client(url, key)

    def cursor(self) -> supabase.create_client:
        return self._instance.table("q_a")

    @st.cache_data
    def query(_self) -> pd.DataFrame:
        cursor = _self.cursor()
        result=cursor.select("*").execute()
        return pd.DataFrame(result.data)
    
    def insert(_self, data):
        # data = """{"question": "a", "answer": "b", "difficulty": 1}"""
        data1 = json.loads(data)
        print(data1)
        cursor = _self.cursor()
        result=cursor.insert(data1).execute()
        return result
    
       