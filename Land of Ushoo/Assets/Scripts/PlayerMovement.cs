using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    [SerializeField] private float speed;
    [SerializeField] private float jumpPower;
    [SerializeField] private LayerMask groundLayer;
    [SerializeField] private LayerMask wallLayer;

    private Rigidbody2D body;
    private Animator anim;
    private BoxCollider2D boxCollider;
    private float horizontalInput;
    PlayerHealth playerHealth;

    private void Awake()
    {
        // Grabs references for rigidbody and animator from object
        body = GetComponent<Rigidbody2D>();
        anim = GetComponent<Animator>();
        boxCollider = GetComponent<BoxCollider2D>();
        playerHealth = GetComponent<PlayerHealth>();
    }

    private void Update()
    {
        horizontalInput = Input.GetAxis("Horizontal");

        // Flip player left and right depending on direction of movement
        if (GetComponent<PlayerCombat>().GetAttackTimer() <= 0 && Alive())
        {
            if (horizontalInput > 0.01f)
                transform.localScale = Vector3.one;
            else if (horizontalInput < -0.01f)
                transform.localScale = new Vector3(-1, 1, 1);
        }

        // Set animator parameters
        anim.SetBool("run", horizontalInput != 0);
        anim.SetBool("grounded", isGrounded());

        bool grounded = isGrounded();

        if (!isWalled() && Alive())
        {
            body.velocity = new Vector2(speed * horizontalInput, body.velocity.y);
        }

        if (Input.GetKey(KeyCode.Space) && grounded && Alive())
            Jump();

    }

    private void Jump()
    {
        body.velocity = new Vector2(body.velocity.x, jumpPower);
        anim.SetTrigger("jump");
    }

    private bool isWalled()
    {
        if (horizontalInput > 0.01f)
        {
            RaycastHit2D raycastHit = Physics2D.BoxCast(boxCollider.bounds.center, boxCollider.bounds.size, 0, Vector2.right, 0.1f, groundLayer);
            return raycastHit.collider != null;
        }
            
        else if (horizontalInput < -0.01f)
        {
            RaycastHit2D raycastHit = Physics2D.BoxCast(boxCollider.bounds.center, boxCollider.bounds.size, 0, Vector2.left, 0.1f, groundLayer);
            return raycastHit.collider != null;
        }

        else { return false; }
    }

    private bool isGrounded()
    {
        Vector3 restrictedBounds = boxCollider.bounds.size;
        restrictedBounds[0] = boxCollider.bounds.size[0] / 2;
        RaycastHit2D raycastHit = Physics2D.BoxCast(boxCollider.bounds.center, restrictedBounds, 0, Vector2.down, 0.1f, groundLayer);
        return raycastHit.collider != null;
    }

    public bool canAttack()
    {
        return true;
    }

    public bool Alive()
    {
        return playerHealth.Alive();
    }
}
