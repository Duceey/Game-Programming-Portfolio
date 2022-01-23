using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TerrainMovement : MonoBehaviour
{
    [SerializeField] private Vector2 startPosition;
    [SerializeField] private Vector2 endPosition;
    [SerializeField] private float speed;

    private Rigidbody2D rb;
    private bool forward = true;
    private Vector2 direction;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        direction = Direction();
    }

    void Update()
    { 
        if (forward)
        {
            rb.velocity = direction * speed;
        }
        else
        {
            rb.velocity = -direction * speed;
        }

        if (Vector2.SqrMagnitude(rb.position - startPosition) > Vector2.SqrMagnitude(direction))
        {
            forward = false;
        }

        if (Vector2.SqrMagnitude(rb.position - endPosition) > Vector2.SqrMagnitude(direction))
        {
            forward = true;
        }

    }

    Vector2 Direction()
    {
        return endPosition - startPosition;
    }
}
