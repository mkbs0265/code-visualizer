def fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def main():
    # Test variables
    x = 10
    y = 20
    result = x + y
    
    # Test function calls
    fib_5 = fibonacci(5)
    
    # Test loops
    numbers = []
    for i in range(5):
        numbers.append(i * 2)
    
    # Test conditionals
    if result > 25:
        message = "Sum is greater than 25"
    else:
        message = "Sum is 25 or less"
    
    # Print results
    print(f"x = {x}, y = {y}")
    print(f"x + y = {result}")
    print(f"5th Fibonacci number: {fib_5}")
    print(f"Numbers: {numbers}")
    print(f"Message: {message}")

if __name__ == "__main__":
    main() 