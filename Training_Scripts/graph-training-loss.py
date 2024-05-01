import pandas as pd
import plotly.express as px

# Initialize lists to store extracted data
batch_sizes = []
gradient_accums = []
losses = []
steps = []
run_ids = []
total_times = []

# Helper variables
current_run_id = 0
current_total_time = ''

# Open and read the file
with open('ChatBot Hyperparameter Tuning.txt', 'r') as file:
    for line in file:
        if line.startswith("Device Batch Size:"):
            current_run_id += 1  # Increment for each new configuration
            parts = line.split()
            batch_size = int(parts[3])
            gradient_accum = int(parts[7])
            step_count = 0  # Reset step count for new run
        elif "{'loss':" in line:
            loss_part = line.split("'loss':")[1].split(',')[0].strip()
            losses.append(float(loss_part))
            step_count += 10
            steps.append(step_count)
            batch_sizes.append(batch_size)
            gradient_accums.append(gradient_accum)
            run_ids.append(current_run_id)  # Assign current run ID
            total_times.append(current_total_time)  # Assign total time of the current run
        elif "Total Time:" in line:
            current_total_time = line.split(":")[1].strip()  # Extract total time for the current run
        elif line.startswith("================================================================================================================"):
            continue  # Move to the next line

# Create a DataFrame from the lists
df = pd.DataFrame({
    'Batch Size': batch_sizes,
    'Gradient Accumulation': gradient_accums,
    'Loss': losses,
    'Step': steps,
    'Run ID': run_ids,
    'Total Time': total_times
})

# Generate a label for each run
df['Run'] = df.apply(lambda row: f'Run {row["Run ID"]} (Batch {row["Batch Size"]} x GradAcc {row["Gradient Accumulation"]}, {row["Total Time"]})', axis=1)

# Plotting the data using Plotly
fig = px.line(df, x="Step", y="Loss", color="Run",
              title="Training Loss Over Steps Across Different Configurations",
              labels={"Loss": "Training Loss", "Step": "Step"},
              markers=True,
              hover_data=["Total Time"])

# Enhance plot layout for better readability
fig.update_layout(
    xaxis_title="Step",
    yaxis_title="Training Loss",
    legend_title="Run Configuration",
    hovermode="x unified"
)

# Display the plot
fig.show()
