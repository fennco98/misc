import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

class RetirementAccount:
    def __init__(self, gross_income, growth_rate, tax_rate):
        self.balance = 0
        self.growth_rate = growth_rate
        self.tax_rate = tax_rate
        self.contributions = []
        # self.make_contribution(gross_income)
        # how can i have this use the child method for the given child classes?

    def make_contribution(self, contribution):
        self.contributions.append(contribution)
        self.balance += contribution

    def get_contributions(self):
        return self.contributions

    def get_contribution_total(self, years):
        contributions_total =[]
        for _ in range(years + 1):
            contributions_total.append(sum(self.contributions[0:years]))
        return self.contributions_total

    def calculate_balance_over_time(self, years, yearly_contribution):
        balances = []
        for _ in range(years + 1):
            balances.append(self.balance)
            self.balance *= (1 + self.growth_rate)
            self.make_contribution(yearly_contribution)
            # should we be making contribution in this loop?
            # I think so, since we don't do it anywhere else
        return balances

class Traditional401k(RetirementAccount):
    # contributions are pre-tax
    # distributions are taxed as income
    def __init__(self, gross_income, growth_rate, tax_rate):
        super().__init__(gross_income, growth_rate, tax_rate)

    def make_contribution(self, contribution):
        cont = contribution
        limit = 22500
        if cont > limit:
            cont = limit
        super().make_contribution(cont)
        # super().make_contribution(cont * (1-self.tax_rate))

    def calculate_balance_over_time(self, years, yearly_contribution):
        balances = super().calculate_balance_over_time(years, yearly_contribution)
        # since distributions are taxed as income, usable balance -= income tax
        balances = [i * (1 - effective_tax_rate) for i in balances]
        return balances

class Roth401k(RetirementAccount):
    # contributions are post-tax
    # distributions are tax free
    def __init__(self, gross_income, growth_rate, tax_rate):
        super().__init__(gross_income, growth_rate, tax_rate)  # No tax on contributions for Roth

    def make_contribution(self, contribution):
        cont = contribution
        limit = 22500
        if cont > limit:
            cont = limit
        # super().make_contribution(cont)
        super().make_contribution(cont * (1-self.tax_rate))

class TraditionalIRA(RetirementAccount):
    # contributions are post tax (technically partially deductible, but not at high incomes)
    # distributions are taxed as income
    def __init__(self, gross_income, growth_rate, tax_rate):
        super().__init__(gross_income, growth_rate, tax_rate)

    def make_contribution(self, contribution):
        cont = contribution
        limit = 6500
        if cont > limit:
            cont = limit
        # super().make_contribution(cont)
        super().make_contribution(cont * (1-self.tax_rate))

    def calculate_balance_over_time(self, years, yearly_contribution):
        balances = super().calculate_balance_over_time(years, yearly_contribution)
        balances = [i * (1 - effective_tax_rate) for i in balances]
        return balances

class RothIRA(RetirementAccount):
    # contributions are post tax
    # distributions are tax-free
    def __init__(self, gross_income, growth_rate, tax_rate):
        super().__init__(gross_income, growth_rate, tax_rate)  # No tax on contributions for Roth

    def make_contribution(self, contribution):
        cont = contribution
        limit = 6500
        if cont > limit:
            cont = limit
        # super().make_contribution(cont)
        super().make_contribution(cont * (1-self.tax_rate))


# Constants
gross_income = 25000  # Gross income for annual contributions
annual_growth_rate = 0.10  # 10% annual growth rate
effective_tax_rate = 0.35  # 30% effective income tax rate
years = 30

# Create retirement accounts
account_401k = Traditional401k(gross_income, annual_growth_rate, effective_tax_rate)
account_roth_401k = Roth401k(gross_income, annual_growth_rate, effective_tax_rate)
account_ira = TraditionalIRA(gross_income, annual_growth_rate, effective_tax_rate)
account_roth_ira = RothIRA(gross_income, annual_growth_rate, effective_tax_rate)

# Get contributions over time for each account
contribution_total_401k = account_401k.get_contribution_total

# Calculate balances over time for each account
balance_401k = account_401k.calculate_balance_over_time(years, gross_income)
balance_roth_401k = account_roth_401k.calculate_balance_over_time(years, gross_income)
balance_ira = account_ira.calculate_balance_over_time(years, gross_income)
balance_roth_ira = account_roth_ira.calculate_balance_over_time(years, gross_income)

# Create plots for each account
years_range = np.arange(0, years + 1)
plt.figure(figsize=(10, 6))
ax = plt.plot(years_range, balance_401k,         label='401(k)',         linestyle='-')
plt.plot(years_range, balance_roth_401k,    label='Roth 401(k)',    linestyle='--')
plt.plot(years_range, balance_ira,          label='IRA')
plt.plot(years_range, balance_roth_ira,     label='Roth IRA')

# Customize the plot
plt.suptitle('Retirement Account Usable Balances Over Time')
formatted_gross_income = '{:,}'.format(gross_income)
real_subtitle =     'Gross annual income devoted to funding each account = $' + formatted_gross_income + '\n' + \
                    'Effective income tax rate = ' + str(effective_tax_rate*100) + '%'
plt.title(real_subtitle, fontsize=8)
plt.xlabel('Years')
plt.ylabel('Effective Account Balance ($)')
# format our y-axis so it's nice whole numbers with commas :)
plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
plt.legend()

# Show the plot
plt.grid(True)
plt.tight_layout()
plt.show()