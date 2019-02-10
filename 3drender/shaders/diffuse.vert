#version 450
layout(location=0) in vec4 position;
layout(location=1) in vec4 color;
layout(location=2) in vec3 normal;

layout(location=1) uniform mat4 model;
layout(location=2) uniform mat4 view;
layout(location=3) uniform mat4 proj;
layout(location=4) uniform vec4 quater;

out vec3 v_color;
out vec3 v_normal;

void main() {
    vec4 w_normal = model * vec4(normal, 0.0);
    v_normal = w_normal.xyz;
    gl_Position = proj * view * model * position;
    float object = 1.3;

	v_color = color.xyz * object;
}
