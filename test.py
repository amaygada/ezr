import os
import pytest
from dumb_vs_smart import main, read_data, guess
import stats
from math import exp

# Create a pytest fixture to set up the real CSV data path
@pytest.fixture
def csv_file():
    # Path to your CSV test file
    return "./data/optimize/config/SS-A.csv"

# Basic Tests
def test_read_data(csv_file):
    # Test the read_data function
    data = read_data(csv_file)
    
    # Check if the data is loaded correctly
    assert data is not None
    assert len(data.rows) > 0  # Ensure data rows are read
    
def test_guess(csv_file):
    # Test the guess function
    data = read_data(csv_file)
    N = 3  # For instance, pick 3 rows
    
    chebyshev_result = guess(N, data)
    
    # Check that we get valid results back from the guess function
    assert len(chebyshev_result.rows) == N
    assert all(isinstance(row, list) for row in chebyshev_result.rows)

# Test for chebyshevs().rows[0] returning the top item
def test_chebyshevs_top_item(csv_file):
    # Test that chebyshevs().rows[0] returns the top item in the sort
    data = read_data(csv_file)
    chebyshev_sorted = data.chebyshevs()  # Assuming chebyshevs returns a sorted dataset
    top_item = chebyshev_sorted.rows[0]   # Retrieve the top item
    all_distances = [data.chebyshev(row) for row in data.rows]
    assert data.chebyshev(top_item) == min(all_distances), "The top item is not the one with the minimum Chebyshev distance."

@pytest.mark.parametrize("N", [20, 30, 40, 50])
def test_smart_dumb_list_lengths(csv_file, N):
    # Test that smart and dumb lists have the correct lengths (N)
    data = read_data(csv_file)

    # Test the dumb approach (exploit with branching)
    dumb = [guess(N, data) for _ in range(20)]  # Run for 20 times
    assert all(len(lst.rows) == N for lst in dumb), f"Dumb list lengths are incorrect for N={N}"

    # Test the smart approach (exploit and explore)
    smart = [data.shuffle().activeLearning(score=lambda B, R: B - R) for _ in range(20)]
    assert len(smart) == 20, "Smart treatment did not run 20 times"
    assert all(isinstance(lst, list) and len(lst) > 0 for lst in smart), f"Smart list lengths is invalid for N={N}"

# Test for running experiment 20 times
def test_run_experiment_20_times(csv_file):
    # Test if the experiment is run 20 times as expected
    data = read_data(csv_file)
    
    # Simulate the smart experiment 20 times
    N = 30  # Example N
    smart_experiments = [data.shuffle().activeLearning(score=lambda B, R: B - R) for _ in range(20)]
    
    # Ensure we have exactly 20 results
    assert len(smart_experiments) == 20, "The smart experiment didn't run 20 times."

    # Simulate the dumb experiment 20 times
    dumb_experiments = [guess(N, data) for _ in range(20)]
    
    # Ensure we have exactly 20 results
    assert len(dumb_experiments) == 20, "The dumb experiment didn't run 20 times."

# Test to ensure that d.shuffle() shuffles data correctly
def test_shuffle_function(csv_file):
    # Test if d.shuffle() really jumbles the data
    data = read_data(csv_file)
    
    original_rows = [row for row in data.rows]  # Make a copy of the original order
    shuffled_data = data.shuffle()  # Shuffle the data
    
    # Check that the data is actually shuffled by comparing it with the original
    assert shuffled_data.rows != original_rows, "Data was not shuffled properly."
    assert sorted(shuffled_data.rows) == sorted(original_rows), "Shuffling altered the data content, not just the order."

# Main Function Tests
def test_main_no_output_file(csv_file):
    # Test the main function with no result file
    main("", csv_file)

    # No specific output to validate here, just ensuring no exceptions occur
    
def test_main_with_output_file(tmp_path, csv_file):
    # Test the main function with an output file
    result_file_name = str(tmp_path / "results")
    os.makedirs(result_file_name, exist_ok=True)
    
    # Run the main function and generate output
    main(result_file_name, csv_file)
    
    # Check if the output file was created
    output_file = result_file_name + "/" + csv_file.split(".csv")[0].replace('/', '_') + ".result"
    assert os.path.isfile(output_file)
    
    # Check that the file is not empty
    with open(output_file, 'r') as f:
        content = f.read()
        assert len(content) > 0  # File should not be empty

# Parameterized test to cover different approaches
@pytest.mark.parametrize("N", [20, 30, 40, 50])
@pytest.mark.parametrize("branch", [False, True])
@pytest.mark.parametrize("what, how", [
    ('exploit', lambda B, R: B - R),
    ('explore', lambda B, R: (exp(B) + exp(R)) / (1E-30 + abs(exp(B) - exp(R))))
])
def test_smart_and_dumb(csv_file, N, branch, what, how):
    # Testing the smart and dumb strategies
    data = read_data(csv_file)
    
    # Exploit Dumb branch logic
    if (what == 'exploit') and branch:
        dumb = [guess(N, data) for _ in range(20)]
        dumb = [data.chebyshev(lst.rows[0]) for lst in dumb]
        assert len(dumb) == 20
        assert all(isinstance(val, float) for val in dumb)
    
    # Test smart approach
    smart = [data.shuffle().activeLearning(score=how) for _ in range(20)]
    smart = [data.chebyshev(lst[0]) for lst in smart]
    
    assert len(smart) == 20
    assert all(isinstance(val, float) for val in smart)