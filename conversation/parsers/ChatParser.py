import xml.etree.ElementTree as ET
import os
import glob

# The subdirectories under which ROUGE-compatible summaries should be output
OUTPUT = 'output/'
REFERENCE = 'reference/'

class EmailParser:
    def __init__(self, overall_dir, debug):
        self.overall_dir = overall_dir
        self.debug_flag = debug

    def corpus(self, partition):
        return '{}/{}/corpus'.format(self.overall_dir, partition)

    def annotation(self, partition):
        return '{}/{}/annotation'.format(self.overall_dir, partition)

    def parse(self, partition):
        threads, thread_labels, thread_names = self.load_data(self.corpus(partition), self.annotation(partition))

        data = {
            'data': threads,
            'labels': thread_labels,
            'names': thread_names
        }

        return data
        
    def load_data(self, corpus_dir, annotation_dir):
        threads, thread_labels, thread_names = self.parse_corpus_and_annotations(corpus_dir, annotation_dir)
        return threads, thread_labels, thread_names

    def parse_corpus_and_annotations(self, corpus_dir, annotation_dir):
        threads = []
        thread_labels = []
        thread_names = []

        for anno_filename in os.listdir(annotation_dir):
            curr_thread = []
            curr_thread_labels = []
            quotes = set()
            number = anno_filename.split('-').[1].split('.')[0]
            anno_file = os.path.join(annotations_dir, anno_filename)
            tree = ET.parse(anno_file)
            root = tree.getroot()
            for p in root.findall('p'):
                for q in p.findall('quote'):
                    quotes.add(q.text.replace('\n', ''))

            corpus_filename = 'corpus-' + number + '.txt'
            corpus_file = os.path.join(corpus_dir, corpus_filename)
            for line in corpus_file.readlines():
                line = line.replace('\n', '')
                curr_thread.append(line)
                for q in quotes:
                    if q.replace(',', '') in line.replace(',', ''):
                        curr_thread_labels.append(1)
                    else:
                        curr_thread_labels.append(0)
            threads.append(curr_thread)
            thread_labels.append(curr_thread_labels)

    def compile_reference_summaries(self):
        with open(self.corpus('val')) as corpus_file, open(self.annotation('val')) as annotations_file:
            annotations = self.parse_annotations(annotations_file)

            output_dir = OUTPUT + REFERENCE

            if os.path.exists(output_dir):
                for f in glob.glob(output_dir + '*'):
                    os.remove(f)
            else:
                os.makedirs(output_dir)

            tree = ET.parse(corpus_file)
            root = tree.getroot()

            for thread_index, thread in enumerate(root):
                listno = thread.find('listno').text
                annotations_list = annotations[listno]
                
                for annotation_index, annotation in enumerate(annotations_list):
                    summary = []
                    
                    for doc in thread.findall('DOC'):
                        text = doc.find('Text')
                        for sent in text:
                            sentence_id = sent.attrib['id']
                            if sentence_id in annotation:
                                summary.append(sent.text + ' ')

                    filename = output_dir + 'thread{}_reference{}.txt'.format(thread_index, annotation_index)
                    with open(filename, 'w') as output_file:
                        output_file.write(''.join(summary))

    def debug(self, output):
        if self.debug_flag:
            print(output)

def flatten(nested_list):
    return [label for thread in nested_list for label in thread]
