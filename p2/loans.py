race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}

class Applicant:
    def __init__(self, age, race):
        self.age = age
        rs = set()
        for r in race:
            if r in race_lookup.keys():
                rs.add(race_lookup[r])
        self.race = rs
    def __repr__(self):
        race_list = list(self.race)
        return f"Applicant('{self.age}', {race_list})"   
    def lower_age(self):
        if '<' in self.age:
            low = self.age.replace('<',"")
        elif '>' in self.age:
            low = self.age.replace('>',"")
        else:
            low = self.age.split("-")[0]
        return int(low)
    def __lt__(self, other):
        return self.lower_age() < other.lower_age()
    
class Loan:
    def __init__(self, fields):
        self.loan_amount = fields["loan_amount"]
        self.property_value = fields["property_value"]
        self.interest_rate = fields["interest_rate"]
        
        if self.loan_amount == "NA" or self.loan_amount == "Exempt":
            self.loan_amount = -1
        
        if self.property_value == "NA" or self.property_value == "Exempt":
            self.property_value = -1
        
        if self.interest_rate == "NA" or self.interest_rate == "Exempt":
            self.interest_rate = -1
            
        self.loan_amount = float(self.loan_amount)
        self.property_value = float(self.property_value)
        self.interest_rate = float(self.interest_rate)
        
        race_list = []
        for i in [1,2,3,4,5]:
            if len(fields[f"applicant_race-{i}"])>0:
                race_list.append(fields[f"applicant_race-{i}"])
        self.applicants = [Applicant(fields["applicant_age"],race_list)]
        
        if fields["co-applicant_age"] != "9999":
            race_list2 = []
            for i in [1,2,3,4,5]:
                if len(fields[f"co-applicant_race-{i}"])>0:
                    race_list2.append(fields[f"co-applicant_race-{i}"])
            self.applicants.append(Applicant(fields["co-applicant_age"],race_list2))  
            
    def __str__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def __repr__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def yearly_amounts(self, yearly_payment):
        assert self.loan_amount >0 and self.interest_rate>0
        amt = self.loan_amount
        i = self.interest_rate

        while amt > 0:
            yield amt
            amt = amt * i*0.01 + amt - yearly_payment
            
import json
from zipfile import ZipFile, ZIP_DEFLATED
from io import TextIOWrapper
from csv import DictReader
    
class Bank:
    def __init__(self,name):
        self.name = name
        with open("banks.json") as f:
            banks = json.load(f)
            for b in banks:
                if b["name"] == self.name:
                    self.lei = b["lei"]
        self.dl = []
        with ZipFile('wi.zip') as zf:
            with zf.open('wi.csv') as csvfile:
                reader = DictReader(TextIOWrapper(csvfile))
                for dic in reader:
                    if dic["lei"] == self.lei:
                        self.dl.append(Loan(dic))
    def __len__(self):
        return len(self.dl)
    def __getitem__(self, lookup):
        return self.dl[lookup]

    