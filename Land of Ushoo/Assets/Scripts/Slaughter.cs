using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Slaughter : MonoBehaviour
{
    [SerializeField] Transform player;
    [SerializeField] float attackAggroRange;
    [SerializeField] float aggroRange;
    [SerializeField] float Speed;
    [SerializeField] float attackRange;
    [SerializeField] int attackDamage;
    [SerializeField] float attackDelay;
    [SerializeField] float attackDamageDelay;

    Rigidbody2D rigidBody2D;
    float attackTimer;
    Animator anim;
    Enemy enemy;
    public Transform attackPoint;
    public LayerMask playerLayer;

    // Start is called before the first frame update
    void Start()
    {
        rigidBody2D = GetComponent<Rigidbody2D>();
        anim = GetComponent<Animator>();
        enemy = GetComponent<Enemy>();
    }

    // Update is called once per frame
    void Update()
    {
        // Finds Actual position
        Vector2 actualPosition = transform.position;
        actualPosition[0] = transform.position[0] + 1;

        // Distance to player
        float distanceToPlayer = Vector2.Distance(actualPosition, player.position);

        attackTimer -= Time.deltaTime;

        if (CanAttack() && Alive())
        {
            if (distanceToPlayer < attackAggroRange)
            {
                Attack();
            }

            else if (distanceToPlayer < aggroRange)
            {
                ChasePlayer();
            }
            else
            {
                StopChasingPlayer();
            }
        }
    }

    bool Alive()
    {
        return enemy.Alive();
    }

    bool CanAttack()
    {
        return attackTimer <= 0;
    }

    void Attack()
    {
        attackTimer = attackDelay;

        if (transform.position.x + 1 < player.position.x)
        {
            if (transform.localScale[0] > 0)
            {
                Vector3 position = transform.localPosition;
                position[0] += 2;
                transform.localPosition = position;
                transform.localScale = new Vector2(-3, 3);
            }
        }
        else
        {
            if (transform.localScale[0] < 0)
            {
                Vector3 position = transform.localPosition;
                position[0] -= 2;
                transform.localPosition = position;
                transform.localScale = new Vector2(3, 3);
            }
        }

        anim.SetBool("walking", false);
        anim.SetTrigger("attack");

        StartCoroutine(DamagePlayer());
    }

    IEnumerator DamagePlayer()
    {
        yield return new WaitForSeconds(attackDamageDelay);

        Collider2D[] hitPlayer = Physics2D.OverlapCircleAll(attackPoint.position, attackRange, playerLayer);

        foreach (Collider2D player in hitPlayer)
        {
            player.GetComponent<PlayerHealth>().TakeDamage(attackDamage);
        }
    }
    void ChasePlayer()
    {
        anim.SetBool("walking", true);

        if (transform.position.x + 1 < player.position.x)
        {
            rigidBody2D.velocity = new Vector2(Speed, 0);
            if (transform.localScale[0] > 0) 
            { 
                Vector3 position = transform.localPosition;
                position[0] += 2;
                transform.localPosition = position;
                transform.localScale = new Vector2(-3, 3);
            }
        }
        else
        {
            rigidBody2D.velocity = new Vector2(-Speed, 0);
            if (transform.localScale[0] < 0)
            {
                Vector3 position = transform.localPosition;
                position[0] -= 2;
                transform.localPosition = position;
                transform.localScale = new Vector2(3, 3);
            }
        }
    }

    void StopChasingPlayer()
    {
        anim.SetBool("walking", false);
        rigidBody2D.velocity = new Vector2(0, 0);
    }
}
