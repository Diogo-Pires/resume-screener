import random

# Country codes with example mobile prefixes
country_codes = {
    "+1": ["202", "303", "415", "646"],        # US
    "+44": ["7400", "7911", "7800"],           # UK
    "+351": ["91", "93", "96"],                # Portugal
    "+33": ["6", "7"],                          # France
    "+49": ["151", "160", "170"],              # Germany
    "+55": ["11", "21", "31", "41"],           # Brazil
    "+34": ["611", "622", "633"],              # Spain
    "+61": ["4"],                               # Australia
    "+81": ["80", "90", "70"],                 # Japan
}

def generate_random_number():
    country = random.choice(list(country_codes.keys()))
    prefix = random.choice(country_codes[country])
    number = ''.join(random.choices("0123456789", k=random.randint(6, 8)))
    return f"{country} {prefix}{number}"

# Generate and print 1000 random phone numbers
phone_numbers = [generate_random_number() for _ in range(1000)]

# Save to file if needed
with open("random_phone_numbers.txt", "w") as f:
    f.write('\n'.join(phone_numbers))

print("Generated 1000 random phone numbers.")