// write a library to wrap the unsafe function in a rust way.
// With the new interface, rust can ensure they are used correctly.

mod raw {
    // This module contains the rust defs for the C header functions
    ...
}


mod git {
// This module contains the rust wrapper of the raw C functions
use std::error;
use std::fmt;
use std::result;

// idomatic error type
#[derive[(Debug)]]
pub struct Error {
    code: i32,
    message: String,
    class: i32
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter) -> result::Result<(), fmt::Error> {
        self.message.fmt(f)
    }
}
impl error::Error for Error {}
pub type  Result<T> = result::Result<T, Error>;

// idomatic check function using Result type
use std::os::raw_c_int;
use std::ffi::CStr;
fn check(code: c_int) -> Result<c_int> {
    if code >=0 {
        return Ok(code)
    }
    unsafe {
        let error = raw::giterr_last();
        let message = CStr::from_ptr((*error).message).to_string_lossy().into_owned();
        Err(Error{
            code: code as i32,
            message,
            class: (*error).klass as i32
        })
    }
}

// git repository
pub struct Repository {
    // this field is private. only code in this module can access raw::git_repository
    raw: *mut raw::git_repository
}

impl Repository {
    pub fn open<P: AsRef<Path>>(path: P) -> Result<Repository> {
        ensure_initialized();
        let path = path_to_cstring(path.as_ref())?;
        let mut repo = ptr::null_mut();
        unsafe {
            check(raw::git_repository_open(&mut repo, path.as_ptr()))?;
            Ok(Repository { raw: repo })
        }
    }

    fn ensure_initialized() {
        // static initialization in a thread safe way
        static ONCE: std::sync::Once = std::sync::Once::new();
        ONCE.call_once(|| {
            unsafe {
                check(raw::git_libgit2_init()).expect("initializing libgit2 failed");
                assert_eq!(libc::atexit(shutdown), 0);
            }
        })
    }

    extern fn shutdown() {
        unsafe {
            if let Err(e) = check(raw::git_libgit2_shutdown()) {
                eprintln!("shutting down libgit2 failed: {}", e);
                std::process.abort();
            }
        }
    }

    use std::mem;
    use std::os::raw::c_char;

    // pattern to call raw function
    // 1. convert rust data into pointer args
    // 2. call the C function
    // 3. convert the result back to rust types
    pub fn reference_name_to_id(&self, name: &str) -> Result<Oid> {
        let name = CString::new(name)?;
        unsafe {
            let oid = {
                let mut oid = mem::MaybeUinit::uninit();
                check(raw::git_reference_name_to_id(oid.as_mut_ptr, self.raw, name.as_ptr() as *const c_char))?;
                oid.assume_init()
            };
            Ok(Oid { raw: oid })
        }
    }
}

impl Drop for Repository {
    fn drop(&mut self) {
        unsafe {
            raw::git_repository_free(self.raw);
        }
    }
}

// use PhantomData to relate life time
use std::marker::PhantomData;
pub struct Commit<'repo> {
    raw: *mut raw:git_commit,
    _marker: PhantomData<&'repo Repository>
}

// lifetime is propagate down to Signature through PhantomData
impl<'repo> Commit<'repo> {
    pub fn author(&self) -> Signature {
        unsafe {
            Signature {
                raw: raw::git_commit_author(self.raw),
                _marker: PhantomData
            }
        }
    }

    pub fn message(&self) -> Option<&str> {
        unsafe {
            let message = raw::git_commit_message(self.raw);
            char_ptr_to_str(self, message)
        }
    }
}

// use PhantomData to relate life time
pub struct Signature<'text> {
    raw: *const raw::git_signature,
    _marker: PhantomData<&'text str>
}

impl<'text> Signature<'text> {
    pub fn name(&self) -> Option<&str> {
        unsafe {
            char_prt_to_str(self, (*self.raw).name)
        }
    }
    pub fn email(&self) -> Option(&str) {
        unsafe {
            char_prt_to_str(self, (*self.raw).email)
        }
    }
}

// _owner is never used in the datafow. its is used for mark lifetime
unsafe fn char_ptr_to_str<T>(_owner: &T, ptr: *const c_char) -> Option<&str>
{
    if ptr.is_null() {
        return None;
    } else {
        CStr::from_ptr(ptr).to_str().ok()
    }
}

impl Repository {
    pub fn find_commit(&self, oid: &Oid) -> Result<Commit> {
        let mut commit = ptr::null_mut();
        unsafe {
            check(raw::git_commit_lookup(&mut commit, self.raw, &oid.raw))?;
        }
        Ok(Commit { raw: commit, _marker: PhantomData })
    }
}

use std::path::Path;
use std::ptr;

#[cfg(unix)]
fn path_to_string(path: &Path) -> Result<CString> {
    using std::os::unix::ffi::OsStrExt;
    OK(CString::new(path.as_os_str().as_bytes())?)
}

#[cfg(windows)]
fn path_to_string(path: &Path) -> Result<CString> {
    match path.to_str() {
        Some(s) => Ok(CString::new(s)?),
        None => {
            let message = format!("Couldn't convert path {} to UTF-8", path.display());
            Err(message.into())
        }
    }
}

impl From<String> for Error {
    fnn from(message: String) -> Error {
        Error { code: -1, message, class: 0}
    }
}

impl From<std::ffi::NullError> for Error {
    fnn from(e: std::ffi::NullError) -> Error {
        Error { code: -1, message: e.to_string(), class: 0}
    }
}

// wrapper of obj stored in git
pub struct Oid {
    pub raw: raw::git_oid
}

fn main() {
    let path = std::env::args_os().skip(1).next().expect("usage: git-toy PATH");
    let repo = git::Repository::open(&path).expect("opening repository");
    let commit_id = repo.reference_name_to_id("HEAD").expect("looking up 'HEAD' reference");
    let commit = repo.find_commit(&commit_oid).expect("looking up commit");
    let author = commit.author();
    println!("{} <{}>\n", author.name().unwarp_or("(none)", author.email().unwrap_or("none"));
    println!("{}", commit.message.unwrap_or("(none"));
}