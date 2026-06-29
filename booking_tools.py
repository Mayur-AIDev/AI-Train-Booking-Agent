import json
from langchain_core.tools import tool

@tool
def check_train_availability(source: str, destination: str, travel_date: str) -> str:
    """Use this tool to search train availability between source and destination for a specific date (YYYY-MM-DD)."""
    try:
        with open("train_db.json", "r") as file:
            trains = json.load(file)
            
        matches = [
            t for t in trains 
            if t["from"].lower() == source.lower() 
            and t["to"].lower() == destination.lower() 
            and t["date"] == travel_date
        ]
    
        if not matches:
            return f"No trains found from {source} to {destination} on {travel_date}."
        
        return json.dumps(matches, indent=2)
    except Exception as e:
        return f"Error reading database: {str(e)}"
    
@tool
def book_train_ticket(train_no: str, seats_to_book: int) -> str:
    """Use this tool to book seats on the specific train by providing the train number and number of seats as an integer."""
    try:
        with open("train_db.json", "r") as file:
            trains = json.load(file)
            
        for train in trains:
            if train["train_no"] == train_no:
                if train["available_seats"] >= seats_to_book:
                    train["available_seats"] -= seats_to_book
                    
                    # Write updates back to the file
                    with open("train_db.json", "w") as file:
                        json.dump(trains, file, indent=2)
                    return f"SUCCESS: Successfully booked {seats_to_book} seats on Train {train_no}. Ticket Status: CONFIRMED."
                else:
                    return f"FAILED: Not enough seats available. Requested: {seats_to_book}, Available: {train['available_seats']}."
                    
        return f"FAILED: Train number {train_no} not found in the system."
    except Exception as e:
        return f"Error processing booking: {str(e)}"
