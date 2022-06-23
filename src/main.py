import os

from memex_logging import memex_logger


def get_list_of_files_to_be_processed(target_directory: str) -> list[str]:
    return os.listdir(target_directory)


class MarkdownToHTMLConverter:
    def __init__(self) -> None:
        pass

    def convert_file_to_html(self, input_file_path: str, output_file_path: str):
        memex_logger.info(f"Converting input file {input_file_path} to HTML at {output_file_path}")
        with open(input_file_path, mode="r") as markdown_file:
            input_file_contents = markdown_file.read()

            with open(output_file_path, mode="x") as output_file:
                output_file.write(input_file_contents)
                output_file.write("\n\nfile has been processed.")


if __name__ == "__main__":
    WORKING_DIRECTORY = "../test/data/markdown/"
    HTML_OUTPUT_DIRECTORY = "../test/test_output/"

    markdown_processor = MarkdownToHTMLConverter()

    files_to_be_processed = get_list_of_files_to_be_processed(WORKING_DIRECTORY)

    for file_name in files_to_be_processed:
        input_path = os.path.join(WORKING_DIRECTORY, file_name)

        file_name_without_extension = os.path.splitext(file_name)[0]
        
        output_path = os.path.join(HTML_OUTPUT_DIRECTORY, file_name_without_extension + ".html")
        markdown_processor.convert_file_to_html(input_path, output_path)

