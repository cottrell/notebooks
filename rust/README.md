# Notes

https://doc.rust-lang.org/rust-by-example/

https://www.vortexa.com/insight/integrating-rust-into-python

https://developers.redhat.com/blog/2017/11/16/speed-python-using-rust#create_a_new_crate

https://github.com/VorTECHsa/rust-python-integration

https://github.com/PyO3/pyo3

https://coursesity.com/free-tutorials-learn/rust

https://www.udemy.com/course/rust-lang

## 2022-03

    mkdir mymod_pyo3
    maturin init  # selectin pyo3
    cargo build --release
    cp target/release/libmymod_pyo3.so mymod_pyo3.so
    ipython
    >>> import mymod_pyo3


rustc to just compile a file
