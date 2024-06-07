from ftfy import fix_text
class Review():
    def __init__(self,stt,text,label):
        self.stt = stt
        self.labels = label
        self.orginalText = text

def read_files(filename):
    documents = list()
    count = 0
    with open(filename,'r',encoding='utf8') as file:
        text1 = file.read()
        for item in text1.split('\n'):
            if item != '':
                item = item.strip()
                if count == 0:
                    stt = fix_text(item)
                    count += 1
                elif count == 1:
                    text = fix_text(item)
                    count += 1
                elif count == 2:
                    labels = fix_text(item)
                    count = 0
                    reviewtemp = Review(stt, text, labels)
                    documents.append(reviewtemp)
    return documents


def convert_data(raw_labels):
    """Converts raw labels into a list of extracted labels.

    This function splits the `raw_labels` string into a list, where each element
    represents a label starting with '{' and ending with '}'.

    Args:
        raw_labels: The string containing raw labels separated by ', {'.

    Returns:
        A list of extracted labels.
    """

    label_list = []
    start = 0
    end = None

    while raw_labels.find('{') != -1:
        end = raw_labels.find('}')
        label_list.append(raw_labels[start:end+1].strip())
        # print(raw_labels[start:end])
        raw_labels = raw_labels[end + 3:]

    return label_list

def check_format(label):
  """Checks if the format of the label is valid.

  Args:
    label: The label to be checked.

  Returns:
    True if the label starts with '{' and ends with '}', False otherwise.
  """

  return label.startswith('{') and label.endswith('}') and len(label.split(', ')) == 2



def main():
    documents = read_files('/workspaces/ABSA_Dataset/Hotel_ABSA/Dev.txt')
    print(len(documents))
    for document in documents:
        for label in convert_data(document.labels):
            assert check_format(label), (document.labels, document.stt)

if __name__ == '__main__':
    main()