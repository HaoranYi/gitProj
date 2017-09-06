from codepy.cgen import FunctionBody, FunctionDeclaration, Typedef, POD, \
    Value, Pointer, Module, Block, Initializer, Assign
from codepy.cgen.cuda import CudaGlobal

mod = Module([
    FunctionBody(
        CudaGlobal(FunctionDeclaration(
            Value("void", "add"),
            arg_decls = [Pointer(POD(dtype, name)) for name in ['tgt', 'op1', 'op2']])),
        Block([
            Initializer(
                POD(numpy.int32, "idx"),
                "threadIdx.x + %d*blockIdx.x"
                % (thread_block_size*block_size)),
            ] = [
                 Assign(
                "tgt[idx+%d]" % (o*thread_block_size),
                "op1[idx+%d] + op2[idx+%d]" % (
                    o*thread_block_size,
                    o*thread_block_size))
            for o in range(block_size)]))])
mod = SourceModule(mod)
