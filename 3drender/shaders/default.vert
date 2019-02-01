#version 450
layout(location=0) in vec4 position;
layout(location=1) in vec4 color;
out vec4 v_color;
layout(location=1) uniform mat4 model;
layout(location=2) uniform mat4 view;
layout(location=3) uniform mat4 proj;
layout(location=4) uniform vec4 quater;

void main() {
    vec4 p = position;
    vec4 g;
    float s = abs(p.y) ;
    if (false && s >= 0.5)
        g = vec4(p.x * s, p.y, p.z * s, p.w);
    else
        g = p;

	gl_Position = proj * view * model * g;
	v_color = color;
}
