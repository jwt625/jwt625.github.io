


# %% interactive cone
import numpy as np
import plotly.graph_objects as go

# Create polar coordinates for circular boundary
k_max = 2  # Maximum wavevector magnitude
theta = np.linspace(0, 2*np.pi, 100)
r = np.linspace(0, k_max, 50)

# Create grid in polar coordinates
T, R = np.meshgrid(theta, r)

# Convert to Cartesian coordinates
k_x = R * np.cos(T)
k_y = R * np.sin(T)

# Calculate omega values for upper cone
omega = np.sqrt(k_x**2 + k_y**2)

# Create figure with minimal styling
fig = go.Figure(go.Surface(
    x=k_x, 
    y=k_y, 
    z=omega,
    colorscale='Viridis',
    opacity=0.5,  # Increased transparency
    showscale=False,  # Disable colorbar
    hoverinfo='none'  # Disable hover info
))

# Configure ultra-clean layout
fig.update_layout(
    title='Light Cone',
    scene=dict(
        xaxis=dict(
            title='kₓ',
            showticklabels=False,
            ticks=""
        ),
        yaxis=dict(
            title='kᵧ',
            showticklabels=False,
            ticks=""
        ),
        zaxis=dict(
            title='ω',
            showticklabels=False,
            ticks=""
        ),
        camera=dict(eye=dict(x=1.5, y=1.5, z=0.8)),
        aspectmode='cube'
    ),
    margin=dict(l=0, r=0, b=0, t=30),
    width=800,
    height=600
)

# Show plot
fig.show()




# %% onto a lattice
import numpy as np
import plotly.graph_objects as go

# Base cone parameters
k_max = 11  # Cone base radius
shift = 4  # Lattice constant

# Generate base cone coordinates (polar)
theta = np.linspace(0, 2*np.pi, 100)
r = np.linspace(0, k_max, 50)
T, R = np.meshgrid(theta, r)
kx_base = R * np.cos(T)
ky_base = R * np.sin(T)
# omega_base = np.sqrt(kx_base**2 + ky_base**2)

# quadratic dispersion
omega_base = (kx_base**2 + ky_base**2)/k_max

# Create lattice points (3x3 grid)
lattice_points = [(i*shift, j*shift) for i in [-2, -1, 0, 1, 2] 
                                for j in [-2, -1, 0, 1, 2]]

# Create figure
fig = go.Figure()

# Add multiple translated cones
for dx, dy in lattice_points:
    fig.add_trace(go.Surface(
        x=kx_base + dx,
        y=ky_base + dy,
        z=omega_base,
        colorscale='Viridis',
        showscale=False,
        opacity=0.25,  # Increased transparency
        hoverinfo='none'
    ))

# Configure ultra-clean layout with expanded view
n_plotRange = 0.5
fig.update_layout(
    title='Photonic Crystal-like Light Cone Array',
    scene=dict(
        xaxis=dict(
            title='kₓ',
            showticklabels=False,
            ticks="",
            range=[-shift*n_plotRange, shift*n_plotRange]  # Expanded view
        ),
        yaxis=dict(
            title='kᵧ',
            showticklabels=False,
            ticks="",
            range=[-shift*n_plotRange, shift*n_plotRange]
        ),
        zaxis=dict(
            title='ω',
            showticklabels=False,
            ticks="",
            range=[0, k_max*0.5]
        ),
        camera=dict(eye=dict(x=2, y=2, z=0.8)),
        aspectmode='manual',  # Changed from 'cube'
        aspectratio=dict(
            x=1,   # Relative x-axis size
            y=1,   # Relative y-axis size
            z=3    # Stretch factor for z-axis (ω)
        )
    ),
    margin=dict(l=0, r=0, b=0, t=30),
    width=800,
    height=1000
)

# Show plot
fig.show()






############## test interactive plot
#%%
%matplotlib widget


#%%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Enable interactive mode
plt.ion()

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # Adjust layout for sliders

x = np.linspace(0, 10, 100)
line, = ax.plot(x, np.sin(x))

# Add sliders
slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03])
slider = Slider(slider_ax, 'Frequency', 0.1, 5.0, valinit=1.0)

def update(val):
    line.set_ydata(np.sin(slider.val * x))
    fig.canvas.draw_idle()  # Update plot without redrawing everything

slider.on_changed(update)
plt.show()

# %%
import plotly.graph_objs as go
from plotly.subplots import make_subplots

fig = make_subplots()
fig.add_trace(go.Scatter(x=[1,2,3], y=[4,5,6]))
fig.update_layout(
    sliders=[{
        "steps": [{"args": [{"y": [i, i+1, i+2]}], "label": i} for i in range(10)]
    }]
)

fig.write_html("../_includes/plot.html", include_plotlyjs="cdn")



# %% phase matching of refraction

import plotly.graph_objects as go
import numpy as np

# Generate circle points (static data)
theta = np.linspace(0, 2*np.pi, 100)
circle1_x = np.cos(theta)
circle1_y = np.sin(theta)
circle2_x = 1.5 * np.cos(theta)
circle2_y = 1.5 * np.sin(theta)

# Create figure with static elements
fig = go.Figure()

# Add persistent circles with legend entries
fig.add_trace(go.Scatter(
    x=circle1_x, y=circle1_y,
    mode='lines',
    line=dict(color='gray', dash='dot'),
    name='n₁ (Medium 1)',
    showlegend=True
))
fig.add_trace(go.Scatter(
    x=circle2_x, y=circle2_y,
    mode='lines', 
    line=dict(color='gray', dash='dash'),
    name='n₂ (Medium 2)',
    showlegend=True
))

# Add permanent legend entries for vectors (never displayed)
fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode='lines+markers',
    line=dict(color='blue', width=2),
    marker=dict(symbol='arrow', size=15),
    name='k₁/k<sub>0</sub> (Refracted)',
    showlegend=True
))
fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode='lines+markers',
    line=dict(color='red', width=2),
    marker=dict(symbol='arrow', size=15),
    name='k₂/k<sub>0</sub> (Incident)',
    showlegend=True
))

# Initialize dynamic elements (hidden from legend)
fig.add_trace(go.Scatter(x=[], y=[], mode='lines+markers', showlegend=False))  # k₁
fig.add_trace(go.Scatter(x=[], y=[], mode='lines+markers', showlegend=False))  # k₂
fig.add_trace(go.Scatter(x=[], y=[], mode='text', showlegend=False))  # status

# Create frames with proper arrow angles
frames = []
theta2_values = np.linspace(0, np.pi/2, 100)

for theta2 in theta2_values:
    k2_x = 1.5 * np.cos(theta2)
    k2_y = 1.5 * np.sin(theta2)
    
    # Calculate angles for arrow orientation (degrees)
    angle_k2 = np.degrees(theta2)
    
    # Phase matching calculation
    if k2_x <= 1.0:
        theta1 = np.arccos(k2_x)
        k1_x, k1_y = np.cos(theta1), np.sin(theta1)
        angle_k1 = np.degrees(theta1)
        status = "Phase Matched"
        status_color = "green"
    else:
        k1_x, k1_y = np.nan, np.nan
        angle_k1 = 0
        status = "Total Internal Reflection"
        status_color = "red"

    frame = go.Frame(
        data=[
            # Static circles (preserve original data)
            go.Scatter(x=circle1_x, y=circle1_y),
            go.Scatter(x=circle2_x, y=circle2_y),
            # k₁ vector
            go.Scatter(
                x=[0, k1_x], y=[0, k1_y],
                line=dict(color='blue', width=2),
                marker=dict(
                    symbol='arrow',
                    size=15,
                    angleref='previous',
                    # angle=angle_k1  # Offset for arrow orientation
                )
            ),
            # k₂ vector
            go.Scatter(
                x=[0, k2_x], y=[0, k2_y],
                line=dict(color='red', width=2),
                marker=dict(
                    symbol='arrow',
                    size=15,
                    angleref='previous',
                    # angle=angle_k2  # Offset for arrow orientation
                )
            ),
            # Status text
            go.Scatter(
                x=[0], y=[1.7],
                mode='text',
                text=[f"<b>{status}</b>"],
                textfont=dict(color=status_color, size=14)
            )
        ],
        name=f"theta_{np.rad2deg(theta2):.1f}"
    )
    frames.append(frame)

# Assign frames to figure
fig.frames = frames

# Configure slider and layout
slider = [dict(
    active=0,
    currentvalue=dict(prefix="θ₂: ", font=dict(size=14)),
    pad=dict(t=50),
    steps=[dict(
        method='animate',
        args=[
            [f"theta_{np.rad2deg(theta2):.1f}"],
            dict(mode='immediate', 
                 frame=dict(duration=100, redraw=True),
                 transition=dict(duration=0))
        ],
        label=f"{np.rad2deg(theta2):.1f}°"
    ) for theta2 in theta2_values]
)]

fig.update_layout(
    title="Phase Matching Condition Demo<br><sub>Adjust θ₂ with slider below</sub>",
    xaxis=dict(
        range=[-1.8, 1.8],
        title="k<sub>x</sub>",
        scaleanchor="y",
        scaleratio=1
    ),
    yaxis=dict(
        range=[-0.1, 1.8],
        title="k<sub>y</sub>"
    ),
    showlegend=True,
    legend=dict(
        x=1.05,
        y=0.5,
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='rgba(0,0,0,0.2)',
        traceorder='normal'
    ),
    sliders=slider,
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        x=0.1,
        y=0,
        buttons=[dict(
            label='▶',
            method='animate',
            args=[None, dict(frame=dict(duration=100, redraw=True), 
                            fromcurrent=True)]
        )]
    )]
)

# Save to HTML
fig.write_html(
    "../_includes/phase_matching_plot.html",
    include_plotlyjs='cdn',
    full_html=False
)


# %% test adding field plot

import plotly.graph_objects as go
import numpy as np

# Parameters
n1 = 1.0
n2 = 1.5
wavelength = 1.0
w0_inc = 10 * wavelength / n2  # Beam width in medium 2

# Generate circle points (static data)
theta = np.linspace(0, 2*np.pi, 100)
circle1_x = np.cos(theta)
circle1_y = np.sin(theta)
circle2_x = 1.5 * np.cos(theta)
circle2_y = 1.5 * np.sin(theta)

# Create figure with dual axes
fig = go.Figure()

# Original phase matching plot elements (Left side)
fig.add_trace(go.Scatter(
    x=circle1_x, y=circle1_y,
    mode='lines',
    line=dict(color='gray', dash='dot'),
    name='n₁ (Medium 1)',
    showlegend=True
))
fig.add_trace(go.Scatter(
    x=circle2_x, y=circle2_y,
    mode='lines', 
    line=dict(color='gray', dash='dash'),
    name='n₂ (Medium 2)',
    showlegend=True
))

# Legend entries for vectors
fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode='lines+markers',
    line=dict(color='blue', width=2),
    marker=dict(symbol='arrow', size=15),
    name='k₁/k<sub>0</sub> (Refracted)',
    showlegend=True
))
fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode='lines+markers',
    line=dict(color='red', width=2),
    marker=dict(symbol='arrow', size=15),
    name='k₂/k<sub>0</sub> (Incident)',
    showlegend=True
))

# Dynamic elements for original plot
fig.add_trace(go.Scatter(x=[], y=[], mode='lines+markers', showlegend=False))  # k₁
fig.add_trace(go.Scatter(x=[], y=[], mode='lines+markers', showlegend=False))  # k₂
fig.add_trace(go.Scatter(x=[], y=[], mode='text', showlegend=False))  # status

# Add dummy heatmap trace for real-space plot (Right side)
fig.add_trace(go.Heatmap(
    x=[], y=[], z=[],
    colorscale='RdBu',
    zmin=-2,
    zmax=2,
    showscale=False,
    xaxis='x2',
    yaxis='y2'
))

# Create coordinate grid for real-space plot
x_real = np.linspace(-20, 20, 150)
y_real = np.linspace(-20, 15, 150)
X, Y = np.meshgrid(x_real, y_real)

# Create frames with proper data
frames = []
theta2_values = np.linspace(0, np.pi/2, 30)

for theta2 in theta2_values:
    # Original k-space calculations
    k2_x = 1.5 * np.cos(theta2)
    k2_y = 1.5 * np.sin(theta2)
    
    # Phase matching calculation
    if k2_x <= 1.0:
        theta1 = np.arccos(k2_x)
        k1_x, k1_y = np.cos(theta1), np.sin(theta1)
        status = "Phase Matched"
        status_color = "green"
        
        # Fresnel calculations
        cos_theta_inc = np.cos(theta2)
        cos_theta_trans = k2_x  # Since k1_x = k2_x and n1=1
        r_TE = (n1*cos_theta_inc - n2*cos_theta_trans)/(n1*cos_theta_inc + n2*cos_theta_trans)
        t_TE = (2*n1*cos_theta_inc)/(n1*cos_theta_inc + n2*cos_theta_trans)
    else:
        k1_x, k1_y = np.nan, np.nan
        status = "Total Internal Reflection"
        status_color = "red"
        r_TE = 1.0
        t_TE = 0.0

    # Real-space field calculation
    phase_inc = k2_x*X + k2_y*Y
    phase_refl = k2_x*X - k2_y*Y
    phase_trans = k1_x*X + k1_y*Y if t_TE != 0 else 0
    
    E_inc = np.exp(-X**2/(2*(w0_inc**2))) * np.exp(1j*phase_inc)
    E_refl = r_TE * np.exp(-X**2/(2*(w0_inc**2))) * np.exp(1j*phase_refl)
    E_trans = t_TE * np.exp(-X**2/(2*(w0_inc*(n2/n1))**2)) * np.exp(1j*phase_trans)
    
    E_total = np.where(Y < 0, E_inc + E_refl, E_trans)
    field_data = np.real(E_total)

    frame = go.Frame(
        data=[
            # Original plot elements
            go.Scatter(x=circle1_x, y=circle1_y),
            go.Scatter(x=circle2_x, y=circle2_y),
            go.Scatter(
                x=[0, k1_x], y=[0, k1_y],
                line=dict(color='blue', width=2),
                marker=dict(symbol='arrow', size=15)
            ),
            go.Scatter(
                x=[0, k2_x], y=[0, k2_y],
                line=dict(color='red', width=2),
                marker=dict(symbol='arrow', size=15)
            ),
            go.Scatter(
                x=[0], y=[1.7],
                mode='text',
                text=[f"<b>{status}</b>"],
                textfont=dict(color=status_color, size=14)
            ),
            # Real-space heatmap
            go.Heatmap(
                x=x_real, y=y_real, z=field_data,
                colorscale='RdBu', zmin=-2, zmax=2,
                xaxis='x2', yaxis='y2'
            )
        ],
        name=f"theta_{np.rad2deg(theta2):.1f}"
    )
    frames.append(frame)

# Configure layout with dual axes
fig.update_layout(
    title="Phase Matching Condition & Beam Dynamics",
    xaxis=dict(
        domain=[0, 0.4],
        range=[-1.8, 1.8],
        title="k<sub>x</sub>",
        scaleanchor="y",
        scaleratio=1
    ),
    yaxis=dict(
        domain=[0.1, 0.9],
        range=[-0.1, 1.8],
        title="k<sub>y</sub>"
    ),
    xaxis2=dict(
        domain=[0.5, 1],
        title="x (λ)",
        anchor='y2'
    ),
    yaxis2=dict(
        domain=[0.1, 0.9],
        title="y (λ)",
        anchor='x2'
    ),
    showlegend=True,
    legend=dict(
        x=1.05,
        y=0.5,
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='rgba(0,0,0,0.2)'
    ),
    sliders=[dict(
        active=0,
        currentvalue=dict(prefix="θ₂: "),
        steps=[dict(
            method='animate',
            args=[
                [f"theta_{np.rad2deg(theta2):.1f}"],
                dict(mode='immediate', frame=dict(duration=100, redraw=True))
            ],
            label=f"{np.rad2deg(theta2):.1f}°"
        ) for theta2 in theta2_values]
    )],
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        x=0.1,
        y=0,
        buttons=[dict(
            label='▶',
            method='animate',
            args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)]
        )]
    )]
)

# Add interface line to real-space plot
fig.add_shape(
    type='line',
    x0=-20, y0=0, x1=20, y1=0,
    line=dict(color='black', width=2, dash='dot'),
    xref='x2', yref='y2'
)

# Assign frames
fig.frames = frames

# Save to HTML
fig.write_html(
    "../_includes/phase_matching_with_beam.html",
    include_plotlyjs='cdn',
    full_html=False
)




# %% testing the heat map field plot alone
import plotly.graph_objects as go
import numpy as np

# Parameters
n1 = 1.0
n2 = 1.5
wavelength = 1.0
theta2 = np.deg2rad(89)  # 30 degrees in radians
w0_inc = 10 * wavelength / n2  # Increased beam width in medium 2

# Wavevector components
k2 = n2  # Magnitude of k2 vector
k2_x = k2 * np.cos(theta2)
k2_y = k2 * np.sin(theta2)

# Phase matching and Fresnel calculations
if k2_x <= n1:
    theta1 = np.arccos(k2_x/n1)
    k1_x = n1 * np.cos(theta1)
    k1_y = n1 * np.sin(theta1)
    # Fresnel coefficients (TE polarization)
    r_TE = (n1*np.cos(theta2) - n2*np.cos(theta1))/(n1*np.cos(theta2) + n2*np.cos(theta1))
    t_TE = (2*n1*np.cos(theta2))/(n1*np.cos(theta2) + n2*np.cos(theta1))
else:
    r_TE = 1.0
    t_TE = 0.0

# Create coordinate grid with expanded range
x = np.linspace(-20, 20, 200)
y = np.linspace(-20, 15, 150)
X, Y = np.meshgrid(x, y)

# Calculate electric fields for all three beams
phase_inc = k2_x * X + k2_y * Y
phase_refl = k2_x * X - k2_y * Y
phase_trans = k1_x * X + k1_y * (Y)  # Transmission in positive y direction

# Gaussian beam profiles (account for refractive index change)
beam_profile_inc = np.exp(-X**2/(2*w0_inc**2))
w0_trans = w0_inc * (n2/n1)  # Beam width in medium 1
beam_profile_trans = np.exp(-X**2/(2*w0_trans**2))

# Field components
E_inc = beam_profile_inc * np.exp(1j * phase_inc)
E_refl = r_TE * beam_profile_inc * np.exp(1j * phase_refl)
E_trans = t_TE * beam_profile_trans * np.exp(1j * phase_trans)

# Combine fields in respective media
E_total = np.where(Y < 0, E_inc + E_refl, E_trans)
field_to_plot = np.real(E_total)

# Create heatmap
fig = go.Figure(data=go.Heatmap(
    x=x,
    y=y,
    z=field_to_plot,
    colorscale='RdBu',
    zmin=-2,
    zmax=2,
    hoverongaps=False
))

# Add interface line and annotations
fig.add_shape(type='line',
    x0=min(x), y0=0, x1=max(x), y1=0,
    line=dict(color='black', width=2, dash='dot')
)

fig.update_layout(
    title=f'Electric Field at θ₂={np.rad2deg(theta2):.1f}°<br>Beam Width: 10λ, Media: n₁=1.0/n₂=1.5',
    xaxis_title='x (λ)',
    yaxis_title='y (λ)',
    width=1000,
    height=800,
    annotations=[
        dict(x=0, y=0.5, text="Medium 1", showarrow=False, yshift=10),
        dict(x=0, y=-0.5, text="Medium 2", showarrow=False, yshift=-10),
        dict(x=15, y=-8, text="Incident", showarrow=False, font=dict(color='blue')),
        dict(x=15, y=-5, text="Reflected", showarrow=False, font=dict(color='red')),
        dict(x=15, y=3, text="Transmitted", showarrow=False, font=dict(color='green'))
    ]
)

fig.show()

# %%
