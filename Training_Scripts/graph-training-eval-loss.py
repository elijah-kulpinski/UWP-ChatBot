import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Initialize lists to store extracted data
batch_sizes = []
gradient_accums = []
losses = []
steps = []
types = []  # To distinguish between training and evaluation losses
run_ids = []

# Helper variables
current_run_id = 0
training_step_counter = 10  # Start from step 10 for the first training loss

# Open and read the file
with open('ChatBot Hyperparameter Tuning.txt', 'r') as file:
    for line in file:
        if line.startswith("Device Batch Size:"):
            current_run_id += 1  # Increment for each new configuration
            parts = line.split()
            batch_size = int(parts[3])
            gradient_accum = int(parts[7])
            training_step_counter = 10  # Reset for each new configuration
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
            steps.append(training_step_counter - 5)  # Assuming eval loss is logged midway between training logs
            batch_sizes.append(batch_size)
            gradient_accums.append(gradient_accum)
            types.append('Evaluation')
            run_ids.append(current_run_id)
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

# Generate a label for each run
df['Configuration'] = df.apply(lambda row: f'Run {row["Run ID"]}: Batch {row["Batch Size"]} x GradAcc {row["Gradient Accumulation"]}', axis=1)

# Use Plotly Express to plot with distinct colors for each configuration and style for training/evaluation
fig = px.line(df, x="Step", y="Loss", color="Configuration", line_dash="Type", 
              title="Training and Evaluation Loss Comparison",
              labels={"Loss": "Loss", "Step": "Training Step"})

# Enhance plot layout
fig.update_layout(
    xaxis_title="Training Step",
    yaxis_title="Loss",
    legend_title="Run Configuration",
    hovermode="x unified"
)

# Display the plot
fig.show()
