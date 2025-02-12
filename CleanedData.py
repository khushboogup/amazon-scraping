import pandas as pd
df=pd.read_csv('product.csv')
df['rating'].fillna(0,inplace=True)
df['price'].fillna(0,inplace=True)
df=df[df['name'].str.contains('Laptop',case=False,na=False)] #this keep those name which contain laptop as word
df = df[~df['name'].str.contains('Tablet|Mobile|Headphone|Charger', case=False, na=False)] # It will delete those row in which name contain Tablet|Mobile|Headphone|Charger
df=df[~df['name'].str.contains('USB|Battery|Mouse|Microphone|Cleaning|Bag',case=False,na=False)]
df=df[~df['name'].str.contains('keyboard|stand|cooler|Protector|Accessories|cover|Memory|Toys|Protection Plan|Laptop RAM',case=False,na=False)]
df=df[~df['name'].str.contains('Case',case=False,na=False)]
df['name'] = df['name'].str.strip()  # Remove leading and trailing spaces
df['name'] = df['name'].str.lower()  # Convert to lowercase for uniformity
df['name'] = df['name'].str.replace(r'\s+', ' ', regex=True)  # Replace multiple spaces with a single space
df['name'] = df['name'].str.normalize('NFKC')  # Normalize Unicode characters
df.to_csv('cleaned.csv',index=False)
