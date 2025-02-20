from graphviz import Digraph

# Create a new directed graph
dot = Digraph("Django_Models", format="png")

# Define model nodes
dot.node("Application", "Application\n- user (FK)\n- name\n- description\n- API_KEY\n- created_ts\n- updated_ts\n- deleted_ts")
dot.node("Permission", "Permission\n- application (FK)\n- name\n- description")
dot.node("Role", "Role\n- application (FK)\n- name\n- description")
dot.node("ApplicationUser", "ApplicationUser\n- application (FK)\n- user (FK)\n- role (FK)\n- joined_ts\n- deleted_ts")

# Define relationships
dot.edge("Application", "Permission", label="1 -> *")
dot.edge("Application", "Role", label="1 -> *")
dot.edge("Role", "Permission", label="M -> M")
dot.edge("Application", "ApplicationUser", label="1 -> *")
dot.edge("ApplicationUser", "User", label="M -> 1", constraint="false")
dot.edge("ApplicationUser", "Role", label="M -> 1")

# Save and render the diagram
diagram_path = "django_models_class_diagram.png"
dot.render(diagram_path, format="png", cleanup=True)

# Display the generated class diagram
diagram_path
