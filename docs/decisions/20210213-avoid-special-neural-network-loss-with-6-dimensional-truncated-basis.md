# Avoid special neural network loss with six dimensional truncated basis

- Status: proposed
- Deciders: fire
- Date: 2021-02-13
- Tags: gan,pytorch

## Context and Problem Statement

The neural network requires special treatment because we use quaternions. The quaternion orientation format is not continuous.

## Decision Drivers <!-- optional -->

- Slow improvement on performance
- Simplicity

## Considered Options

- Basis 3x3 matrix
- Quaternion
- Euler
- 6D Truncation 3x3 Basis

## Decision Outcome

Choose 6D Truncation 3x3 basis because its theory is the simplest, and the paper mathematically proved it was accurate.

### Positive Consequences <!-- optional -->

- Better training gain
- The code is simpler to understand

### Negative Consequences <!-- optional -->

- Work to change to new representation

## Pros and Cons of the Options <!-- optional -->

### Basis 3x3 matrix

Basis 3x3 matrix.

- Good, because continuous
- Bad, because it uses nine rather than six floats.
- Bad, because space inefficient

### Quaternion

The status quo is the Quaternion.

- Good, because it is standard
- Good, because the status quo
- Bad, because it has poles.

### Euler

- Bad, no.
- … <!-- numbers of pros and cons can vary -->

### 6D Truncation 3x3 Basis

A basis is a 3x3 matrix. The Basis is normalized.

```c++
//x_raw is the X Axis / first row of the basis
//y_raw is the Y Axis / second row of the basis.

// On the Continuity of Rotation Representations in Neural Networks
// arXiv:1812.07035
Basis compute_rotation_matrix_from_ortho_6d(Vector3 x_raw, Vector3 y_raw) {
    Vector3 x = x_raw.normalized();
    Vector3 z = x.cross(y_raw);
    z = z.normalized();
    Vector3 y = z.cross(x);
    Basis basis;
    basis.set_axis(Vector3::AXIS_X, x);
    basis.set_axis(Vector3::AXIS_Y, y);
    basis.set_axis(Vector3::AXIS_Z, z);
    return basis;
}
```

- Good, because it's space-efficient with six floats
- Bad, because it's not standard

## Links <!-- optional -->

- https://arxiv.org/pdf/1812.07035.pdf
