#version 450
in vec2 TexCoord;
out vec4 fragColor;
uniform sampler2D tex;

void main() {
	vec4 blend = texture(tex, TexCoord);
    fragColor = blend;
}
