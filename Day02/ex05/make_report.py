from config import *
from analytics import Research


def main():
    r = Research(filepath)
    num_observations = len(r.data)
    lst = r.calc.counts()
    heads = lst[1]
    tails = lst[0]
    heads_prob, tails_prob = r.calc.fractions(lst)
    pred = r.calc.predict_random(num_of_steps)
    heads_pred, tails_pred = tuple(sum(elem) for elem in zip(*pred))
    text = template.format(
        num_observations,
        tails, heads,
        heads_prob, tails_prob,
        num_of_steps,
        tails_pred, heads_pred
        )
    r.calc.save_file(text, output_file)


if __name__ == '__main__':
    main()