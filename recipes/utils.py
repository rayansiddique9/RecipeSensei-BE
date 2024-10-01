"""This module sets up the gemini model for recipe generation api.
"""
import os
import google.generativeai as genai


def getGeminiModel():
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model

