#version 450
layout(location=0) in vec4 position;
layout(location=1) in vec4 color;
out vec4 v_color;
layout(location=1) uniform mat4 model;
layout(location=2) uniform mat4 view;
layout(location=3) uniform mat4 proj;
layout(location=4) uniform vec4 quater;

void main()
{
    gl_Position =  proj * view *  model * position;
	v_color = color;
}
