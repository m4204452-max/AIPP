# TGNPDCL Electricity Bill Calculator

def calculate_energy_charges(units, customer_type):
    # Energy charges based on customer type and consumption slabs
    domestic_slabs = [
        (0, 50, 1.95),
        (51, 100, 3.00),
        (101, 200, 4.50),
        (201, float('inf'), 7.50)
    ]
    
    commercial_slabs = [
        (0, 100, 6.50),
        (101, 200, 7.50),
        (201, float('inf'), 8.50)
    ]
    
    industrial_slabs = [
        (0, 200, 7.00),
        (201, 400, 8.00),
        (401, float('inf'), 9.00)
    ]
    
    total_charge = 0
    remaining_units = units
    
    if customer_type.lower() == 'domestic':
        slabs = domestic_slabs
    elif customer_type.lower() == 'commercial':
        slabs = commercial_slabs
    else:  # industrial
        slabs = industrial_slabs
    
    for lower, upper, rate in slabs:
        if remaining_units <= 0:
            break
        
        slab_units = min(remaining_units, upper - lower + 1)
        total_charge += slab_units * rate
        remaining_units -= slab_units
        
        if upper == float('inf'):
            break
    
    return total_charge

def calculate_fixed_charges(customer_type, connected_load):
    # Fixed charges based on customer type and connected load
    if customer_type.lower() == 'domestic':
        return connected_load * 35  # Rs. 35 per kW
    elif customer_type.lower() == 'commercial':
        return connected_load * 65  # Rs. 65 per kW
    else:  # industrial
        return connected_load * 95  # Rs. 95 per kW

def calculate_customer_charges(customer_type):
    # Customer charges based on category
    charges = {
        'domestic': 30,
        'commercial': 50,
        'industrial': 100
    }
    return charges.get(customer_type.lower(), 30)

def calculate_electricity_duty(energy_charges):
    # Electricity duty is typically 6% of energy charges
    return energy_charges * 0.06

def print_bill(customer_name, customer_type, previous_reading, current_reading, connected_load):
    print("\n" + "="*50)
    print("           TGNPDCL ELECTRICITY BILL")
    print("="*50)
    
    print(f"\nCustomer Name: {customer_name}")
    print(f"Customer Type: {customer_type.title()}")
    print(f"Connected Load: {connected_load} kW")
    print(f"Previous Reading: {previous_reading}")
    print(f"Current Reading: {current_reading}")
    
    # Calculate units consumed
    units = current_reading - previous_reading
    print(f"Units Consumed: {units}")
    
    # Calculate different charges
    energy_charges = calculate_energy_charges(units, customer_type)
    fixed_charges = calculate_fixed_charges(customer_type, connected_load)
    customer_charges = calculate_customer_charges(customer_type)
    electricity_duty = calculate_electricity_duty(energy_charges)
    
    # Calculate total bill
    total_bill = energy_charges + fixed_charges + customer_charges + electricity_duty
    
    print("\nBill Details:")
    print("-"*50)
    print(f"Energy Charges: Rs. {energy_charges:.2f}")
    print(f"Fixed Charges: Rs. {fixed_charges:.2f}")
    print(f"Customer Charges: Rs. {customer_charges:.2f}")
    print(f"Electricity Duty: Rs. {electricity_duty:.2f}")
    print("-"*50)
    print(f"Total Amount: Rs. {total_bill:.2f}")
    print("="*50)
    
    return total_bill

def main():
    print("TGNPDCL Electricity Bill Calculator")
    print("-"*35)
    
    # Get customer details
    customer_name = input("Enter Customer Name: ")
    while True:
        customer_type = input("Enter Customer Type (Domestic/Commercial/Industrial): ").lower()
        if customer_type in ['domestic', 'commercial', 'industrial']:
            break
        print("Invalid customer type! Please try again.")
    
    # Get meter readings
    while True:
        try:
            previous_reading = float(input("Enter Previous Meter Reading: "))
            current_reading = float(input("Enter Current Meter Reading: "))
            if current_reading >= previous_reading:
                break
            print("Current reading must be greater than or equal to previous reading!")
        except ValueError:
            print("Please enter valid numeric readings!")
    
    # Get connected load
    while True:
        try:
            connected_load = float(input("Enter Connected Load (in kW): "))
            if connected_load > 0:
                break
            print("Connected load must be greater than 0!")
        except ValueError:
            print("Please enter a valid numeric value!")
    
    # Generate and print the bill
    print_bill(customer_name, customer_type, previous_reading, current_reading, connected_load)

if __name__ == "__main__":
    main()
