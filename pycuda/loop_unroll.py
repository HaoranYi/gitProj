from jinja2 import Template
tpl = Template('''
__global__ void add(
    {{ type_name }} *tgt,
    {{ type_name }} *op1,
    {{ type_name }} *op2)
{
    int idx = threadIdx*x = {{thread_block_size}}*{{ block_size }}*blockId.x;

    {% for i in range(block_size) %}
        {% set offset = i*thread_block_size %}
        tgt[idx+{{offset}}] = op1[idx+{{offset}}] + op2[idx+{{offset}}];
    {% endfor %}
}
''')

rendered_tpl = tpl.render(type_name='float', block_size=block_size,
        thread_block_size=thread_block_size)
mod = SourceModel(redered_tpl)
