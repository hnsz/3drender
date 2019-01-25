#version 450
in vec2 TexCoord;
in vec4 v_color;
out vec4 fragColor;
uniform sampler2D tex;

void main() {
    vec4 r = vec4(v_color.x, 1.0, 1.0, 1.0) ;
    r.x = 1.0;
	fragColor = vec4(texture(tex, TexCoord).xyz, 0.4) * r;
}
