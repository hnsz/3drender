#version 450
in vec2 TexCoord;
in vec4 v_color;
out vec4 fragColor;
layout(location=0) uniform sampler2D tex;

void main() {
	vec4 blend = texture(tex, TexCoord);
    fragColor = blend * v_color;
}
