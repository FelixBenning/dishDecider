# DishDecider

## Kategorien:

e.g. lasagne (spinat, kürbis)

## Data Structure

```yml
dishes:
  lasagne:
    weight: 2
    variants:
      spinach-lasagne:
        weight: 1
      pumpkin-lasagne:
        weight: 1
  curry:
    weight: 3
    variants: 
      thai:
      ...
  potatosoup:
    weight: 1
    variants: {}
```

## Algo

- adjust probability weights:
  - remove probability of previous meal (and reduce from same category?)
  - add 1/n^2 to every dish
  - increase probability for chain meals (potato variants?) - bratkartoffeln only get positive probability after a different potato dish?