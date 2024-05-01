import pandas as pd
import plotly.express as px

# Function to apply simple moving average for smoothing
def smooth_series(series, window_size):
    return series.rolling(window=window_size, min_periods=1, center=True).mean()

# Initialize lists to store extracted data
batch_sizes = []
gradient_accums = []
losses = []
steps = []
types = []  # To distinguish between training and evaluation losses
run_ids = []

# Helper variables
current_run_id = 0

# Open and read the file
with open('ChatBot Hyperparameter Tuning.txt', 'r') as file:
    for line in file:
        if line.startswith("Device Batch Size:"):
            current_run_id += 1  # Increment for each new configuration
            parts = line.split()
            batch_size = int(parts[3])
            gradient_accum = int(parts[7])
            training_step_counter = 10  # Initialize step counter for training losses
            evaluation_step_counter = 25  # Initialize step counter for evaluation losses
        elif "{'loss':" in line:  # Training loss
            loss_part = line.split("'loss':")[1].split(',')[0].strip()
            losses.append(float(loss_part))
            steps.append(training_step_counter)
            batch_sizes.append(batch_size)
            gradient_accums.append(gradient_accum)
            types.append('Training')
            run_ids.append(current_run_id)
            training_step_counter += 10  # Increment by 10 for each training loss step
        elif "'eval_loss':" in line:  # Evaluation loss
            loss_part = line.split("'eval_loss':")[1].split(',')[0].strip()
            losses.append(float(loss_part))
            steps.append(evaluation_step_counter)  # Set correct step for evaluation loss
            batch_sizes.append(batch_size)
            gradient_accums.append(gradient_accum)
            types.append('Evaluation')
            run_ids.append(current_run_id)
            evaluation_step_counter += 25  # Increment by 25 for each evaluation step
        elif line.startswith("================================================================================================================"):
            continue  # Move to the next line

# Create a DataFrame from the lists
df = pd.DataFrame({
    'Batch Size': batch_sizes,
    'Gradient Accumulation': gradient_accums,
    'Loss': losses,
    'Step': steps,
    'Type': types,
    'Run ID': run_ids
})

# Apply smoothing
window_size = 5  # Adjust this based on your data and desired smoothing level
df['Smoothed Loss'] = df.groupby(['Run ID', 'Type'])['Loss'].transform(lambda x: smooth_series(x, window_size))

# Generate a label for each run
df['Configuration'] = df.apply(lambda row: f'Run {row["Run ID"]}: Batch {row["Batch Size"]} x GradAcc {row["Gradient Accumulation"]}', axis=1)

# Use Plotly Express to plot with distinct colors for each configuration and style for training/evaluation, using the smoothed loss
fig = px.line(df, x="Step", y="Smoothed Loss", color="Configuration", line_dash="Type",
              title="Training and Evaluation Loss Comparison (Smoothed)",
              labels={"Smoothed Loss": "Loss", "Step": "Step"})

# Enhance plot layout
fig.update_layout(
    xaxis_title="Step",
    yaxis_title="Loss",
    legend_title="Run Configuration",
    hovermode="x unified"
)

# Display the plot
fig.show()
