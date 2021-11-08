using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    [SerializeField] public float speed;
    [SerializeField] public float rotationSpeed;

    private Rigidbody2D rb;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        // Player Rotational Movement
        Vector3 rotation = new Vector3(0, 0, -Input.GetAxisRaw("Horizontal") * rotationSpeed * Time.deltaTime);
        transform.Rotate(rotation);

        // Start Player
        if (rb.velocity == Vector2.zero && Input.GetKeyDown("space")) 
        {
            rb.velocity = Direction() * speed;
        }
    }

    void OnCollisionEnter2D(Collision2D collision2D)
    {
        Vector2 direction = Direction();
        Vector3 normal = collision2D.contacts[0].normal;

        if (Vector3.Angle(direction, normal) > 90)
        {
            rb.velocity = -direction * speed;
        } else if (Vector3.Angle(-direction, normal) > 90)
        {
            rb.velocity = direction * speed;
        } else { rb.velocity = normal * speed; }
    }

    Vector2 Direction()
    {
        float angle = transform.localEulerAngles.z / 180 * Mathf.PI;

        return new Vector2(Mathf.Cos(angle), Mathf.Sin(angle));
    }
}