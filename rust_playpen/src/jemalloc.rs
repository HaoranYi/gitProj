// [dependencies]
// jemallocator = "0.3.2"
// jemalloc-ctl = "0.3.2"
// [dependencies.jemalloc-sys]
// version = "0.3.2"
// features = ["stats", "profiling", "unprefixed_malloc_on_supported_platforms"]
// [profile.release]
// debug = true
//

// to run (on demand malloc statistics)
// export MALLOC_CONF=prof:true && a.out
// jeprof --show-bytes --pdf a.out ./profile.out > ./profile.pdf

use jemalloc_ctl::{Access, AsName};
use jemallocator;
use std::collections::HashMap;
#[global_allocator]
static ALLOC: jemallocator::Jemalloc = jemallocator::Jemalloc;
const PROF_ACTIVE: &'static [u8] = b"prof.active\0";
const PROF_DUMP: &'static [u8] = b"prof.dump\0";
const PROFILE_OUTPUT: &'static [u8] = b"profile.out\0";
fn set_prof_active(active: bool) {
    let name = PROF_ACTIVE.name();
    name.write(active).expect("Should succeed to set prof");
}
fn dump_profile() {
    let name = PROF_DUMP.name();
    name.write(PROFILE_OUTPUT)
        .expect("Should succeed to dump profile")
}
fn main() {
    set_prof_active(true);
    let mut buffers: Vec<HashMap<i32, i32>> = Vec::new();
    for _ in 0..100 {
        buffers.push(HashMap::with_capacity(1024));
    }
    set_prof_active(false);
    dump_profile();
}
