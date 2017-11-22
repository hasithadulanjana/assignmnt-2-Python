from __future__ import print_function
import sys
from abc import ABCMeta, abstractmethod
import re
import datetime as date
from rule_chcker import RuleChecker

# Tim
class IFileValidator(metaclass=ABCMeta):
    @abstractmethod
    def check_data_set(self, data_set):
        pass

    @abstractmethod
    def check_line(self, employee_attributes):
        pass

    @abstractmethod
    def check_all(self, employee_attributes):
        pass

    @abstractmethod
    def check_birthday(self, birthday):
        pass

    @abstractmethod
    def check_birthday_against_age(self, birthday, age):
        pass


class Validator(IFileValidator):

    # Tim
    def __init__(self):
        self.id_rule = "^[A-Z][0-9]{3}$"
        self.gender_rule = "^(M|F)$"
        self.age_rule = "^[0-9]{2}$"
        self.sales_rule = "^[0-9]{3}$"
        self.bmi_rule = "^(Normal|Overweight|Obesity|Underweight)$"
        self.salary_rule = "^[0-9]{2,3}$"
        self.birthday_rule = "^[1-31]-[1-12]-[0-9]{4}$"
        self.attributes = {"EMPID", "GENDER", "AGE", "SALES", "BMI", "SALARY", "BIRTHDAY"}
        self.attr =self.rules.get_data()
        self.number_of_attributes = len(self.attributes)


    # Tim
    def check_data_set(self, data_set):
        # Should be of form [{EMPID: B12, GENDER: M, AGE: 22, etc}, {EMPID: 55Y, GENDER: F, etc}]
        if len(data_set) == 0:
            print('The data was empty', file=sys.stderr)
            return False
        else:
            for employee in data_set:
                if not self.check_line(employee):
                    print('One or more of the lines of data was invalid', file=sys.stderr)
                    return False
        # Failing to invalidate is a success
        return True

    # Tim
    def check_line(self, employee_attributes):
        # Should be of form {EMPID: B12, GENDER: M, AGE: 22, etc}
        for attribute in self.attributes:
            if attribute not in employee_attributes:
                print('Missing attribute: {}'.format(attribute), file=sys.stderr)
                return False
        try:
            if not self.check_all(employee_attributes):
                return False
        except TypeError:
            print('The data was not bundled correctly', file=sys.stderr)
            return False
        # Failing to invalidate is a success
        return True

    # Rosemary
    def check_all(self, employee_attributes):
        emp_attr = employee_attributes
        for attribute in emp_attr:
            if not self.check_field(attribute, emp_attr[attribute]):
                return False
        return True

    def check_birthday(self, birthday):
        try:
            day_month_year = birthday.split("-")
            day = int(day_month_year[0])
            month = int(day_month_year[1])
            year = int(day_month_year[2])
            date.datetime(year, month, day)
            return True
        except ValueError:
            print('The date was invalid', file=sys.stderr)
            return False
        except AttributeError:
            print('The date was in an invalid format', file=sys.stderr)
            return False

    # Tim
    def check_birthday_against_age(self, birthday, age):

        if not self.check_birthday(birthday):
            return False
        else:
            day_month_year = birthday.split("-")
            day = int(day_month_year[0])
            month = int(day_month_year[1])
            year = int(day_month_year[2])
            # adding age because we just want to compare month and day
            birth = date.datetime(year, month, day)
            today = date.datetime.today()
            if birth.month < today.month:
                # Had a birthday already this year
                return int(age) == today.year - year
            elif birth.month == today.month and birth.day < today.day:
                # Had a birthday already this year (this month)
                return int(age) == today.year - year
            else:
                # Hasn't had a birthday yet this year.
                return int(age) == today.year - year - 1

    # Tim
    def check_in_attributes(self, query_attribute):
        try:
            return query_attribute.upper() in self.attributes
        except AttributeError:
            return False

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=0)
