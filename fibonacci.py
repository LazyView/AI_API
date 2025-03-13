def fibonacci_sequence(n):
    """
    Calculate the Fibonacci sequence up to n terms.
    
    The Fibonacci sequence is a series of numbers where each number is the sum
    of the two preceding ones, usually starting with 0 and 1.
    
    Args:
        n (int): The number of terms to generate in the sequence.
               Must be a positive integer.
    
    Returns:
        list: A list containing the Fibonacci sequence up to n terms.
    
    Raises:
        ValueError: If n is not a positive integer.
    """
    # Input validation
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Input must be a positive integer")
    
    # Handle special cases
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1]
    
    # Initialize the sequence with the first two numbers
    sequence = [0, 1]
    
    # Generate the remaining terms in the sequence
    for i in range(2, n):
        # Each new term is the sum of the two previous terms
        next_term = sequence[i-1] + sequence[i-2]
        sequence.append(next_term)
    
    return sequence


# Example usage
if __name__ == "__main__":
    # Test with different values
    print(fibonacci_sequence(1))   # [0]
    print(fibonacci_sequence(2))   # [0, 1]
    print(fibonacci_sequence(10))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    
    # Get user input
    try:
        n_terms = int(input("Enter the number of Fibonacci terms to generate: "))
        result = fibonacci_sequence(n_terms)
        print(f"Fibonacci sequence with {n_terms} terms: {result}")
    except ValueError as e:
        print(f"Error: {e}")