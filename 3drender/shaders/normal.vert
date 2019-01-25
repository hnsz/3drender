#version 450
in vec4 position;
in vec4 color;
in vec2 texCoord;
out vec4 v_color;
out vec2 TexCoord;
uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;


void main() {


    v_color = color;
	gl_Position = proj * view * model * position;
    TexCoord = texCoord;
}
