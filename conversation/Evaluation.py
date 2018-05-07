import subprocess
import re

class Evaluation:
    def rouge_evaluation(self):
        # Run ROUGE evaluation
        rouge_result = subprocess.run(['java', '-jar', 'rouge2-1.2.1.jar'], stdout=subprocess.PIPE)
        rouge = rouge_result.stdout.decode('utf-8')

        # Decode ROUGE output to produce averages
        results = {
            'L': [],
            '1': [],
            '2': []
        }

        for line in rouge.splitlines():
            metric_match = re.search('^ROUGE-(.).*', line)
            average_match = re.search('.*Average_F:(.......).*', line)
            if metric_match:
                results[metric_match.group(1)].append(average_match.group(1))

        #  Generate sums
        result = ''
        for metric, data in results.items():
            total = 0
            for point in data:
                total += float(point)
            result += '{}: {}'.format(metric, total / len(data))

        print(result)