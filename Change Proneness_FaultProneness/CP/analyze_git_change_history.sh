# Bash script (head_analyze_full_file_name.sh)
#!/bin/bash
# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <project_name> <project_path> <output_csv_path>"
    exit 1
fi

project_name=$1
project_path=$2
csv_file=$3
original_dir=$(pwd)

# Create output directory if it doesn't exist
output_dir=$(dirname "$csv_file")
mkdir -p "$output_dir"

# Create the CSV file with headers first
echo "Filename,Changes,TotalCommits,Insertions,Deletions" > "$csv_file"
if [ $? -ne 0 ]; then
    echo "Error: Unable to create CSV file at $csv_file"
    exit 1
fi

# Change to the project directory
if ! cd "$project_path"; then
    echo "Error: Unable to change directory to $project_path"
    exit 1
fi

# Get list of all Python files that have been modified
git_files=$(git ls-files "*.py")

# Analyze each Python file
for file in $git_files; do
    # Skip if file doesn't exist
    if [ ! -f "$file" ]; then
        continue
    fi

    # Get the commit hash where the file was first created
    creation_hash=$(git log --diff-filter=A --format=%H -- "$file" | tail -1)
    
    if [ -z "$creation_hash" ]; then
        continue
    fi

    # Calculate metrics
    # Count actual changes (number of commits that modified the file)
    changes=$(git log --follow --format=%H -- "$file" | wc -l)
    
    # Count total commits since file creation
    total_commits=$(git rev-list --count $creation_hash..HEAD)
    
    # Get insertion and deletion statistics
    stat_output=$(git diff --stat $creation_hash..HEAD -- "$file")
    
    # Extract insertions and deletions
    insertions=$(echo "$stat_output" | grep -o '[0-9]* insertion' | awk '{print $1}')
    deletions=$(echo "$stat_output" | grep -o '[0-9]* deletion' | awk '{print $1}')
    
    # Default to 0 if no insertions or deletions found
    insertions=${insertions:-0}
    deletions=${deletions:-0}
    
    # Append to CSV file
    echo "$file,$changes,$total_commits,$insertions,$deletions" >> "$csv_file"
    
    echo "Processed $file - Changes: $changes, Total Commits: $total_commits"
done

cd "$original_dir"
echo "Analysis complete for $project_name. Results saved to $csv_file"