CC = gcc
src_top_dir = .
src_lib_dir = $(src_top_dir)/lib
src_pylog_dir = $(src_lib_dir)/pylog
src_clog_dir = $(src_lib_dir)/clog

dst_top_dir = /usr/local/lib/misc-tools
dst_lib_dir = $(dst_top_dir)/lib
dst_pylog_dir = $(dst_lib_dir)/pylog
dst_clog_dir = $(dst_lib_dir)/clog

dst_bin_dir = /usr/local/bin

src_misc_script = $(src_top_dir)/scripts/python_script/misc.py
dst_misc_script = $(dst_bin_dir)/misc

src_fast_script = $(src_top_dir)/scripts/python_script/fast.py
dst_fast_script = $(dst_bin_dir)/fast

nothing:

install:
	mkdir $(dst_top_dir) -p
	mkdir $(dst_lib_dir) -p
	mkdir $(dst_pylog_dir) -p
	mkdir $(dst_clog_dir) -p
	\cp -rf $(src_pylog_dir)/* $(dst_pylog_dir)
	\cp -rf $(src_misc_script) $(dst_misc_script)
	\cp -rf $(src_fast_script) $(dst_fast_script)

uninstall:
	rm -rf $(dst_top_dir)
	rm -rf $(dst_misc_script) $(dst_fast_script)
