#version 450
in vec4 position;
in vec2 texCoord;
out vec2 TexCoord;
uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;


void main() {


	gl_Position = proj * view * model * position;
    TexCoord = texCoord;
}
