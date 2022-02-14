from unittest.mock import patch, sentinel

import pytest

from wp_original_img_finder import file_is_src_of, find_derived_filenames, main


def test_file_is_src_of():
    derivatives = [
        "/ownpath/wp-content/uploads/2022/sample_file-150x150",
        "/ownpath/wp-content/uploads/2022/sample_file-300x141",
        "/ownpath/wp-content/uploads/2022/sample_file-768x362",
    ]
    for derivative in derivatives:
        assert file_is_src_of(
            "/ownpath/wp-content/uploads/2022/sample_file",
            derivative)


def test_file_is_not_src_of():
    src = "/ownpath/sample_file"
    assert not file_is_src_of(src, "/ownpath/sample_file_sub/xyz")
    assert not file_is_src_of(src, "/ownpath/sample_file/xyz")
    assert not file_is_src_of(src, "/ownpath/sample_file/-150x150")
    assert not file_is_src_of(src, "/ownpath/sample_file/150x150")


def test_find_derived_filenames():
    src_derivatives = find_derived_filenames([
        "/x/uploads/2022/afile.webp",
        "/x/uploads/2022/afile-150x150.webp",
        "/x/uploads/2022/afile-300x141.webp",
        "/x/uploads/2022/afile-768x362.webp",
    ])
    assert src_derivatives == {
        "/x/uploads/2022/afile.webp": [
            "/x/uploads/2022/afile-150x150.webp",
            "/x/uploads/2022/afile-300x141.webp",
            "/x/uploads/2022/afile-768x362.webp"
        ]
    }


def test_find_derived_filenames_in_3_branches():
    src_derivatives = find_derived_filenames([
        "/x/afile.webp",
        "/x/afile-150x150.webp",
        "/x/afile-300x141.webp",
        "/x/afile-768x362.webp",
        "/x/afile-92x92.webp",
        "/y/sub1/afile.webp",
        "/y/sub1/afile-200x100.webp",
        "/y/sub1/afile-600x282.webp",
        "/y/sub1/afile-768x362.webp",
        "/z/afile-1x20.webp",
        "/z/afile-1x20-200x100.webp",
        "/z/afile-1x20-600x282.webp",
        "/z/afile-1x20-768x362.webp",
    ])
    assert src_derivatives == {
        "/x/afile.webp": ["/x/afile-150x150.webp", "/x/afile-300x141.webp",
                          "/x/afile-768x362.webp", "/x/afile-92x92.webp"],
        "/y/sub1/afile.webp": ["/y/sub1/afile-200x100.webp",
                               "/y/sub1/afile-600x282.webp",
                               "/y/sub1/afile-768x362.webp"],
        "/z/afile-1x20.webp": ["/z/afile-1x20-200x100.webp",
                               "/z/afile-1x20-600x282.webp",
                               "/z/afile-1x20-768x362.webp"]}


def test_find_derived_filenames_2_in_single_folder():
    src_derivatives = find_derived_filenames([
        "/src1/wp-c/ups/2022/eg_1.webp",
        "/src1/wp-c/ups/2022/eg_1-150x150.webp",
        "/src1/wp-c/ups/2022/eg_1-300x141.webp",
        "/src1/wp-c/ups/2022/eg_1-768x362.webp",
        "/src1/wp-c/ups/2022/eg_2.jpg",
        "/src1/wp-c/ups/2022/eg_2-150x150.jpg",
        "/src1/wp-c/ups/2022/eg_2-300x141.jpg",
        "/src1/wp-c/ups/2022/eg_2-768x362.jpg"
    ])
    assert src_derivatives == {
        "/src1/wp-c/ups/2022/eg_1.webp": [
            "/src1/wp-c/ups/2022/eg_1-150x150.webp",
            "/src1/wp-c/ups/2022/eg_1-300x141.webp",
            "/src1/wp-c/ups/2022/eg_1-768x362.webp"],
        '/src1/wp-c/ups/2022/eg_2.jpg': [
            '/src1/wp-c/ups/2022/eg_2-150x150.jpg',
            '/src1/wp-c/ups/2022/eg_2-300x141.jpg',
            '/src1/wp-c/ups/2022/eg_2-768x362.jpg']
    }


def test_find_derived_filenames_originator_last():
    src_derivatives = find_derived_filenames([
        "/src1/wp-c/ups/2022/eg_1-150x150.webp",
        "/src1/wp-c/ups/2022/eg_1-300x141.webp",
        "/src1/wp-c/ups/2022/eg_1-768x362.webp",
        "/src1/wp-c/ups/2022/eg_1.webp",
        "/src1/wp-c/ups/2022/eg_2-150x150.jpg",
        "/src1/wp-c/ups/2022/eg_2-300x141.jpg",
        "/src1/wp-c/ups/2022/eg_2-768x362.jpg",
        "/src1/wp-c/ups/2022/eg_2.jpg",
    ])
    assert src_derivatives == {
        "/src1/wp-c/ups/2022/eg_1.webp": [
            "/src1/wp-c/ups/2022/eg_1-150x150.webp",
            "/src1/wp-c/ups/2022/eg_1-300x141.webp",
            "/src1/wp-c/ups/2022/eg_1-768x362.webp"],
        '/src1/wp-c/ups/2022/eg_2.jpg': [
            '/src1/wp-c/ups/2022/eg_2-150x150.jpg',
            '/src1/wp-c/ups/2022/eg_2-300x141.jpg',
            '/src1/wp-c/ups/2022/eg_2-768x362.jpg']
    }


def test_find_derived_filenames_same_names_in_multiple_formats():
    src_derivatives = find_derived_filenames([
        "/src1/wp-c/ups/2022/eg_1.webp",
        "/src1/wp-c/ups/2022/eg_1-150x150.webp",
        "/src1/wp-c/ups/2022/eg_1-300x141.webp",
        "/src1/wp-c/ups/2022/eg_1-768x362.webp",
        "/src1/wp-c/ups/2022/eg_1.jpg",
        "/src1/wp-c/ups/2022/eg_1-150x150.jpg",
        "/src1/wp-c/ups/2022/eg_1-768x362.jpg"
    ])
    assert src_derivatives == {
        "/src1/wp-c/ups/2022/eg_1.webp": [
            "/src1/wp-c/ups/2022/eg_1-150x150.webp",
            "/src1/wp-c/ups/2022/eg_1-300x141.webp",
            "/src1/wp-c/ups/2022/eg_1-768x362.webp"],
        "/src1/wp-c/ups/2022/eg_1.jpg": [
            "/src1/wp-c/ups/2022/eg_1-150x150.jpg",
            "/src1/wp-c/ups/2022/eg_1-768x362.jpg"]
    }


class PreemptiveAnsibleException(Exception):
    """
    Preempting is required so fail_json returns immediately.
    """
    pass


@patch("wp_original_img_finder.AnsibleModule", autospec=True)
def test_main_with_forced_fail(mock_AnsibleModule):
    mock_AnsibleModule.return_value.fail_json.side_effect = PreemptiveAnsibleException
    mock_AnsibleModule.return_value.params = {
        "path": "fail me"
    }
    with pytest.raises(PreemptiveAnsibleException):
        main()
    mock_AnsibleModule.return_value.fail_json.assert_called_once_with(
        failed=True, msg='You requested this to fail', changed=False,
        path_argument="fail me")


@patch("wp_original_img_finder.os.path.exists", return_value=False)
@patch("wp_original_img_finder.AnsibleModule", autospec=True)
def test_main_with_bad_path(mock_AnsibleModule, mock_exists):
    mock_AnsibleModule.return_value.fail_json.side_effect = PreemptiveAnsibleException
    mock_AnsibleModule.return_value.params = {
        "path": sentinel.impossible_path
    }
    with pytest.raises(PreemptiveAnsibleException):
        main()
    mock_AnsibleModule.return_value.fail_json.assert_called_once_with(
        failed=True, msg='Path not present on target.', changed=False,
        path_argument=sentinel.impossible_path)
    mock_exists.assert_called_once_with(sentinel.impossible_path)


@patch("wp_original_img_finder.os.path.exists", autospec=True, return_value=True)
@patch("wp_original_img_finder.AnsibleModule", autospec=True)
@patch(
    "wp_original_img_finder.get_dirs_and_files",
    autospec=True,
    return_value=(["dir1", "dir1/dir2"], ["dir1/file1", "dir1/file2"]))
@patch(
    "wp_original_img_finder.find_derived_filenames",
    autospec=True,
    return_value={"dir1/masterfile": []})
def test_main(mock_find_derived_filenames, mock_get_dirs_and_files, mock_AnsibleModule, mock_exists):
    mock_AnsibleModule.return_value.params = {
        "path": sentinel.dir0
    }
    main()
    mock_AnsibleModule.return_value.exit_json.assert_called_once_with(
        changed=False,
        path_argument=sentinel.dir0,
        directories=["dir1", "dir1/dir2"],
        master_files=["dir1/masterfile"]
    )

