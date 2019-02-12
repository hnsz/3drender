#version 450
layout(location=0) in vec4 position;
layout(location=1) in vec4 color;
layout(location=2 )in vec2 texCoord;
out vec2 TexCoord;
out vec4 v_color;
layout(location=1) uniform mat4 model;
layout(location=2) uniform mat4 view;
layout(location=3) uniform mat4 proj;


void main() {

    v_color = color;
	gl_Position = proj * view * model * position;
    TexCoord = texCoord;
}
