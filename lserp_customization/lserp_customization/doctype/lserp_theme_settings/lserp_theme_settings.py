# Copyright (c) 2024, LEAPSYS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
from bs4 import BeautifulSoup
import re


class LSERPThemeSettings(Document):
    @frappe.whitelist()
    def extract_colors_from_url(self):
        if not self.website_url:
            frappe.throw("Please provide a Website URL.")
        
        try:
            url = self.website_url if self.website_url.startswith('http') else f"https://{self.website_url}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract theme-color meta tag
            theme_color_tag = soup.find('meta', attrs={'name': 'theme-color'})
            if theme_color_tag and theme_color_tag.get('content'):
                primary_hex = theme_color_tag.get('content')
                self.primary_color = primary_hex
                self.sidebar_background = primary_hex
                frappe.msgprint(f"Extracted Primary Color {primary_hex} from meta tags.")
                return

            # Fallback: Extract CSS hex colors from style tags
            styles = " ".join([style.text for style in soup.find_all('style')])
            # rudimentary hex matcher
            hex_colors = re.findall(r'#(?:[0-9a-fA-F]{3}){1,2}\b', styles)
            
            if hex_colors:
                # Get most common hex (simple approach)
                from collections import Counter
                most_common = Counter(hex_colors).most_common(1)[0][0]
                self.primary_color = most_common
                self.sidebar_background = most_common
                frappe.msgprint(f"Extracted roughly dominant color {most_common} from stylesheet.")
            else:
                frappe.msgprint("Could not find obvious theme colors. Please set manually.")

        except Exception as e:
            frappe.throw(f"Error fetching URL: {str(e)}")

    def validate(self):
        if self.active_theme == "LS Theme":
            self.primary_color = "#E1251B" # Example LEAPSYS Red
            self.secondary_color = "#1D1D1B"
            self.text_color = "#333333"
            self.background_color = "#FFFFFF"
            self.sidebar_background = "#E1251B"
        elif self.active_theme == "Enummo Theme":
            self.primary_color = "#0047AB" # Example Enummo Blue
            self.secondary_color = "#00Bfff"
            self.text_color = "#212529"
            self.background_color = "#F8F9FA"
            self.sidebar_background = "#0047AB"
