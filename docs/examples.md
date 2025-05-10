# Example 1: Basic Stock Flow"
# A simple stock and flow example"

Start(100)
Start > Middle @ 10
Middle > End @ 5"""


# Example 2: Hiring Pipeline
# A model of a company hiring pipeline",

[Candidates] > PhoneScreens @ 25
PhoneScreens > Onsites @ Conversion(0.5)
Onsites > Offers @ Conversion(0.5)
Offers > Hires @ Conversion(0.7)
Hires > Employees @ Conversion(0.9)
Employees(5)
Employees > Departures @ Leak(0.05)


# Example 3: Customer Acquisition and Churn
# Model of customer acquisition and retention"

[PotentialCustomers] > EngagedCustomers @ 100
# Initial Integration Flow
EngagedCustomers > IntegratedCustomers @ Leak(0.5)
# Baseline Churn Flow
IntegratedCustomers > ChurnedCustomers @ Leak(0.1)
# Experience Deprecation Flow
IntegratedCustomers > DeprecationImpactedCustomers @ Leak(0.5)
# Reintegrated Flow
DeprecationImpactedCustomers > IntegratedCustomers @ Leak(0.9)
# Deprecation-Influenced Churn
DeprecationImpactedCustomers > ChurnedCustomers @ Leak(0.1)"""
