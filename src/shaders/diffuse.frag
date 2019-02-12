#version 450
in vec3 v_color;
in vec3 v_normal;
out vec4 fragColor;
struct Light {
    vec3 direction;
    vec3 color;
    float ambient;
    float diffuse;
};

void main() {
    float factor;
    vec4 diffuse_color;
    vec4 ambient_color;



    Light light = {{-10.0, 20.0, 10.0}, {.5,.5,.5}, 0.1, .1};


    factor = dot(normalize(v_normal), light.direction);
    if(factor > 0) {
        diffuse_color = vec4(light.color * light.diffuse * factor, 1);
    }
    else {
        diffuse_color = vec4(0,0,0,0);
    }
    ambient_color = vec4(light.color * light.ambient, 1);


    fragColor = vec4(v_color, 1) * (ambient_color + diffuse_color);
}
