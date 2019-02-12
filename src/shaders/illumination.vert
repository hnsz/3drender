#version 450
layout(location=0) in vec4 position;
layout(location=1) in vec4 color;
layout(location=2) in vec3 normal;
out vec3 v_color;
layout(location=1) uniform mat4 model;
layout(location=2) uniform mat4 view;
layout(location=3) uniform mat4 proj;
layout(location=4) uniform vec4 quater;

void main() {
    vec4 norm = proj * view * model * vec4(normal.xyz, 0.0);
    vec4 light = proj * view *  vec4(10.0, 1.0, 20.0, 1.0);
    gl_Position = proj * view * model * position;
    float i = dot(normalize(light.xyz), normalize(norm.xyz));
    vec3 color_o;
    vec3 color_l;
    vec3 color_a;

    float I = 2.3;
    float amb = 1.4;
    float object = 1.3;
    float direct = 0.0;
    if( i > 0)
	    direct = i * I;
	else
	    direct = 0.0;

    color_o = color.xyz * object;
    color_l = vec3(1,1,1) * direct;
    color_a = vec3(.4, .4, .4);


	v_color =  color_o * color_l * color_a;
}
