import heapq

class OrderBook:
    def __init__(self):
        self.active_orders = {}  # Store order ID -> price mapping
        self.max_heap = []  # Max heap to keep track of maximum prices
        self.invalid_heap_entries = set()  # Set to track removed entries from the active_orders
    
    def add_order(self, order_id, price):
        self.active_orders[order_id] = price
        # Push the negative price (for max heap behavior) and order_id into the heap
        heapq.heappush(self.max_heap, (-price, order_id))
    
    def delete_order(self, order_id):
        if order_id in self.active_orders:
            # Mark this heap entry as invalid
            self.invalid_heap_entries.add(order_id)
            del self.active_orders[order_id]
    
    def get_max_price(self):
        # Clean up the heap of invalid entries
        while self.max_heap and self.max_heap[0][1] in self.invalid_heap_entries:
            heapq.heappop(self.max_heap)
        # Return the current maximum price, if available
        if self.max_heap:
            return -self.max_heap[0][0]
        return None

def process_orders(filename):
    order_book = OrderBook()
    time_weighted_sum = 0.0
    total_time = 0
    last_time = None
    last_max_price = None
    
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            timestamp = int(parts[0])
            operation = parts[1]
            order_id = int(parts[2])
            
            if operation == 'I':  # Insert operation
                price = float(parts[3])
                order_book.add_order(order_id, price)
            elif operation == 'E':  # Erase operation
                order_book.delete_order(order_id)
            
            current_max_price = order_book.get_max_price()
            
            if last_time is not None and current_max_price != last_max_price:
                duration = timestamp - last_time
                if last_max_price is not None:
                    time_weighted_sum += last_max_price * duration
                    total_time += duration
            
            last_time = timestamp
            last_max_price = current_max_price
    
    # Calculate the time-weighted average maximum price
    if total_time > 0:
        return time_weighted_sum / total_time
    return 0

# Usage:
filename = 'input.txt'
average_price = process_orders(filename)
print(f"Time-weighted average maximum price: {average_price}")
